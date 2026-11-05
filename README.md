winpak is a file distribution & deployment system that allows for multiple operations with files and/or directories
it utilizes base64 in order to iterate directories and encode any file it meets to base64, putting the dump into a file with the ".pak" extension

as an example, let's say you have a directory named "someDirectory", with the following file tree:
```
someDirectory
  | someSubDirectory
    | subDirectoryFile.txt
  | directoryFile.txt
```
you then run "winpak build someDirectory", and it turns into a single file - someDirectory.pak - which will probably look something like this:
```
[/* MKDIRS */]
someDirectory
someDirectory\someSubDirectory
[/* END */]

[/* FILEWRITE */]
someDirectory\directoryFile.txt
SGVsbG8gV29ybGQhIChkaXJlY3RvcnlGaWxlLnR4dCk=
[/* END */]

[/* FILEWRITE */]
someDirectory\someSubDirectory\subDirectoryFile.txt
R29vZGJ5ZSBXb3JsZCEgKHN1YkRpcmVjdG9yeUZpbGUudHh0KQ==
[/* END */]

[/* CLEAN-TARGS */]
someDirectory
[/* END */]
```
then, you move the .pak file into an other directory, let it be named "repository", and run "winpak updMan repository" so it generates a JSON manifest for the said directory
after, you run "winpak host IP:PORT repository", and while the HTTP server is running, anyone that can connect to your IP will be able to download the file, as long as they have winpak installed
to install the file, you need to run "winpak install IP:PORT packageName" (in our case, packageName will be someDirectory, because the manifest updater wrote it this way into the manifest)
as the file finishes downloading, you can run "winpak deploy filename" (in our case, filename will be someDirectory.pak)
and then you'll have the same filetree as in the first example on the computer that downloaded the package

recently added, you can also inspect what's inside of a .pak file by running "winpak inspect [dirs/files/cmds/clean/file]"
for example, running "winpak inspect someDirectory.pak files" will output:
```
someDirectory\directoryFile.txt
someDirectory\someSubDirectory\subDirectoryFile.txt
```
and running "winpak inspect someDirectory.pak file someDirectory\directoryFile.txt" will output:
```
Hello World! (directoryFile.txt)
```
since that is the base64 string earlier decoded to a normal one
