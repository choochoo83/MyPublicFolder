# copy a file test.py from github.com into abc.py on my system in command line:
1. Select the file you need from github list then click on "raw"
2. Copy the raw URL
curl -o abc.py https://raw.githubusercontent.com/choochoo83/MyPublicFolder/main/Test.py

# copy a versioning file test.py from github.com into abc.py on my system in command line:
1. Go to github.com/test.py and browse its history into the commit version you need
2. Browse file
3. Select the test.py in the list which is running in the old version
4. Click on "raw" and copy the raw URL
curl -o abc.py https://raw.githubusercontent.com/choochoo83/MyPublicFolder/d0c02e5cc4ab7444b2b8d4c2dd001aee740618c5/Test.py
