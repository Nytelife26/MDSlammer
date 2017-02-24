# Necessary imports
import hashlib
import io
import sys
import os
import getpass
import time
import base64

# Backwards compatibility
getin = raw_input if sys.version_info < (3, 0) else input

# Main function        
def main():
    try:
        print("Welcome to MDSlammer - a checksum verifier built in Python.") # Friendly welcome message
        print("(C) Nytelife26 [Tyler J Russell] 2017-present") 
        fp = getin("What file would you like to validate? ") # Asking what file they would like to validate
        fn = fp.split("\\") # Turning fp into a list that uses "\\" as the point of split under a variable called fn.
        temp_fname = fn[len(fn) - 1] # Getting the last object in fn and setting that as temp_fname. This allows us to get the name of the file alone if the user has entered a directory to prevent runtime errors later on.
        fnom = temp_fname.split("/") # Just incase they used something like "../something.something" instead of something like "C:\SomeDir\Anything.anything", we use "/" as a splitting point too.
        fname = fnom[len(fnom) - 1] # Getting the real, real last object now
        fbase = hash(fname) # Getting a hashed version of the filename.
        check_md5 = getin("What is the MD5 validation hash you have been given? Leave blank for none: ").split() # Getting the MD5 hash
        check_md5 = ''.join(check_md5) # Eliminating the possibility of spaces messing up validation
        check_sha256 = getin("What is the SHA256 validation hash you have been given? Leave blank for none: ").split() # Getting the SHA256 hash
        check_sha256 = ''.join(check_sha256) # Eliminating the possibility of spaces messing up validation
        if check_md5 == "": # Checking if the user doesn't want to validate MD5
            check_md5 = None # Setting the according variable
        if check_sha256 == "": # Checking if the user doesn't want to validate SHA256
            check_sha256 = None # Setting the according variable
            
        try: 
            with io.open(fp, 'rb') as file_to_validate: # Opening the file
                data = file_to_validate.read() # Reading the contents of the file
                md5_returned = hashlib.md5(data).hexdigest() if check_md5 is not None else "You specified not to check MD5" # Getting the actual MD5 hash of the file if the user wants to check MD5, if not, we set it to a simple string that specifies they didn't want to check
                sha_returned = hashlib.sha256(data).hexdigest() if check_sha256 is not None else "You specified not to check SHA256" # Getting the actual SHA256 hash of the file if the user wants to check SHA256, if not, we set it to a simple string that specifies they didn't want to check
        except Exception as e: # Just in case the file doesn't exist or we have some other exception
            print("Error while opening file '{}'. Technical info:\n{}".format(fp, e))
        
        # Confirming that we opened the file successfully
        print("File opened and read successfully.")
        
        # Basic if statements to check whether the actual hash matches with the user's provided checksum
        if check_md5 is not None and check_md5 == md5_returned: 
            md5_status = "MD5 validated successfully"
        elif check_md5 is not None and check_md5 != md5_returned:
            md5_status = "MD5 failed to validate. Please re-download the file or download a legitimate copy if you obtained it from a non-official site."
        elif check_md5 is None:
            md5_status = "MD5 did not attempt validation."
        else:
            md5_status = "MD5 validation status unknown. Assume false."
            
        if check_sha256 is not None and check_sha256 == sha_returned:
            sha_status = "SHA256 validated successfully"
        elif check_sha256 is not None and check_sha256 != sha_returned:
            sha_status = "SHA256 failed to validate. Please re-download the file or download a legitimate copy if you obtained it from a non-official site."
        elif check_sha256 is None:
            sha_status = "SHA256 did not attempt validation."
        else:
            sha_status = "SHA256 validation status unknown. Assume false."
            
        # Results page
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S") # Getting the current time so we can log that too, since timestamp is always useful information
        logfile = str("{}.log".format(fbase)) # Setting the name of the file to log the results to.
        print("------------------------------RESULTS------------------------------")
        print("Info:") # Basic information
        print("Filename - {}".format(fname)) # Name of the file that was checked
        print("Time of check - {}".format(timestamp)) # Timestamp of the check
        print("-------------------------------------------------------------------")
        print("MD5:") # MD5 results 
        print("MD5 to check - {}".format(check_md5)) # User-provided MD5 hash
        print("Actual MD5 checksum - {}".format(md5_returned)) # The hash of the actual file
        print("MD5 status - {}".format(md5_status)) # Whether the file does or does not match the checksum / whether it is or is not an official copy.
        print("-------------------------------------------------------------------")
        print("SHA256:") # SHA256 results
        print("SHA256 to check - {}".format(check_sha256)) # User-provided SHA256 hash
        print("Actual SHA256 checksum - {}".format(sha_returned)) # The hash of the actual file
        print("SHA256 status - {}".format(sha_status)) # Whether the file does or does not match the checksum / whether it is or is not an official copy.
        print("-------------------------------------------------------------------")
        
        if not os.path.isdir("{}\\logs".format(os.getcwd())): # Checking whether the log directory exists or not
            print("Logs directory does not exist. Creating it now.") # Tells the user that we are creating the log directory
            os.mkdir("{}\\logs".format(os.getcwd())) # Creating the log directory if it does not exist
            
        with io.open("{}\\logs\\{}".format(os.getcwd(), logfile), 'w+') as outfile: # Opening the log file and creating it if it does not exist
            # Writing the log file. The log file will not be all on one line like it is in the code since we are using \n [line breaks]
            outfile.write("------------------------------RESULTS------------------------------\nInfo:\nFilename - {}\nTime of check - {}\n-------------------------------------------------------------------\nMD5:\nMD5 to check - {}\nActual MD5 checksum - {}\nMD5 status - {}\n-------------------------------------------------------------------\nSHA256:\nSHA256 to check - {}\nActual SHA256 checksum - {}\nSHA256 status - {}\n-------------------------------------------------------------------".format(fname, timestamp, check_md5, md5_returned, md5_status, check_sha256, sha_returned, sha_status)) 
            
        print("These results have been outputted to '{}\\logs\\{}' for future reference.".format(os.getcwd(), logfile)) # Confirming that we wrote the log file and telling them which file it is
        
        # End of the program
        
        getpass.getpass("Press enter to continue.") # Acts like "pause" in Batch.
        exit("MDSlam finished. Exiting...") # Exiting the program
    except KeyboardInterrupt: # Replacing Python's scary error when you hit CTRL+C with a custom, more subtle one.
        exit("Exiting...")
    except Exception as e: # In case of errors that we didn't catch in the code [these are unlikely, but just in case]
        print("\nWhoops! Looks like we hit a snag!") # Making it seem more friendly
        print("DEBUG INFO: Stacktrace -\n{}".format(e)) # Printing technical info for more advanced users.
        exit() # Exiting the program safely
        
# Running the main loop / starting the program
main()
