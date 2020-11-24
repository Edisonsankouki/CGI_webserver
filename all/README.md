# The CGI webserver

## The whole design for setting up webserver.

First rendered the configuration file and Setting uo the file path and the execuate command for the CGI programs. 
Set up a socket webserver with the port we have just rendered. When the client request accepted, we fork here for the first time (in order to handle multiple connections and concurent connection using the child process to handle each requests). if we are in the child process, first we set up the environment variable, and then handle different types of output which is requested by the client. if we are in the parent, just continue the loop.







## The static file handling

Return the file according to the request type. if contains the According-encoding, and if the encoding message is gzip we will return the compressed data. if the file type is undefined, return the default html. if the file can not be found , return 404 error.


## The cgi program handling

Fork again to use the child process to execute the cgi program and redirect the output using pipe, to send it back to parent. if gzip in the According-encoding, return compressed data. If the cgi goes into error, return 500 internal not found. if the cgi contains http/content message, remain it.
