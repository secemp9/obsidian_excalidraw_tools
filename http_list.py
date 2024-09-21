import sys
import webbrowser
import http.server
import socketserver
import os
import urllib
import html
import io

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080  # Use the first argument as the port number, or use 8080 if no argument is provided

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().
        """
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None
        list = [f"{entry}" for entry in list]
        # print(list)
        list.sort(key=lambda a: a.lower())
        r = []
        try:
            displaypath = urllib.parse.unquote(self.path, errors='surrogatepass')
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(path)
        displaypath = html.escape(displaypath, quote=False)
        enc = sys.getfilesystemencoding()
        title = f"Directory listing for {displaypath}"
        r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                 '"http://www.w3.org/TR/html4/strict.dtd">')
        r.append('<html>\n<head>')
        r.append(f'<meta http-equiv="Content-Type" '
                 f'content="text/html; charset={enc}">')
        r.append(f'<title>{title}</title>\n</head>')
        r.append('<body>\n<h1>Directory listing for %s</h1>' % displaypath)
        r.append('<hr>\n<ul>')
        for name in list:
            fullname = os.path.join(path, name)
            # print(fullname, name)
            displayname = f"http://127.0.0.1:{port}{displaypath}{name}"
            linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = f"http://127.0.0.1:{port}{displaypath}{name}/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = f"http://127.0.0.1:{port}/{name}@"
                # print(displayname)
                # Note: a link to a directory displays with @ and links with /
            # displayname = "http://127.0.0.1:8080/" + name
            # print("displayname:", displayname, "linkname:", linkname, "name:", name)
            r.append('<li><a href="%s">%s</a></li>'
                     % (urllib.parse.quote(linkname, errors='surrogatepass'),
                        html.escape(displayname, quote=False)))
        r.append('</ul>\n<hr>\n</body>\n</html>\n')
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f

with socketserver.TCPServer(("127.0.0.1", port), CustomHandler) as httpd:
    print(f"Serving on http://127.0.0.1:{port}")
    webbrowser.open(f"http://127.0.0.1:{port}", new=2)
    httpd.serve_forever()
