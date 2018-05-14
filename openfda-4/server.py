import http.server
import socketserver
import json
import http.client

PORT = 8000
socketserver.TCPServer.allow_reuse_address = True


class OpenFDA_HTML():
    def html_visual(self, list1):
        intro = "<!doctype html>" + "\n" + "<html>" + "\n" + "<body>" + "\n" "<ul>" + "\n"
        end = "</ul>" + "\n" + "</body>" + "\n" + "</html>"

        with open("drug.html", "w") as f:
            f.write(intro)
            for element in list1:
                element1 = "<li>" + element + "</li>" + "\n"
                f.write(element1)
            f.write(end)


HTML = OpenFDA_HTML()


class OpenFDA_Client():
    def search(self, drug, limit):
        headers = {"User-Agent": "http-client"}
        conn = http.client.HTTPSConnection("api.fda.gov")
        url_search = "/drug/label.json?search=active_ingredient:" + drug + "&" + "limit=" + limit
        conn.request("GET", url_search, None, headers)
        r1 = conn.getresponse()
        drugs_raw = r1.read().decode("utf-8")
        conn.close()
        drug = json.loads(drugs_raw)
        drug_1 = drug
        return drug_1


Client = OpenFDA_Client()


class OpenFDA_Parser():
    def drug_data(self, drug_1, list1):
        for i in range(len(drug_1["results"])):
            if 'active_ingredient' in drug_1["results"][i]:
                list1.append(drug_1["results"][i]["active_ingredient"][0])
            else:
                list1.append("Unknown")


Parser = OpenFDA_Parser()


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):

        try:

            if self.path == '/':
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("search.html", "r") as f:
                    data = f.read()
                    self.wfile.write(bytes(data, "utf8"))

            elif "search" in self.path:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                list1 = []

                if "&" not in self.path:
                    limit = "10"
                    params = self.path.split("?")[1]
                    drug = params.split("&")[0].split("=")[1]

                    one = Client.search_drug(drug, limit)
                    Parser.drug_data(one, list1)

                elif "&" in self.path:
                    params = self.path.split("?")[1]
                    drug = params.split("&")[0].split("=")[1]
                    limit = params.split("&")[1].split("=")[1]

                    if not limit:
                        limit = "10"

                    one = Client.search(drug, limit)
                    Parser.drug_data(one, list1)

                HTML.html_visual(list1)

                with open("drug.html", "r") as f:
                    file = f.read()

                self.wfile.write(bytes(file, "utf8"))

            elif "secret" in self.path:
                self.send_response(401)
                self.send_header("WWW-Authenticate", "Basic realm='OpenFDA Private Zone")
                self.end_headers()

            elif "redirect" in self.path:
                self.send_response(302)
                self.send_header("Location", "http://localhost:8000/")
                self.end_headers()

            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("error.html", "r") as f:
                    file = f.read()
                self.wfile.write(bytes(file, "utf8"))

        except KeyError:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("error.html", "r") as f:
                file = f.read()
            self.wfile.write(bytes(file, "utf8"))

        return


Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
