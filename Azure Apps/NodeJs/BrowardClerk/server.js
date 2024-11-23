import path from 'path';
import { fileURLToPath } from 'url';
import http from 'http';
import express from "express";
import { Server } from "socket.io";
import fetch from "node-fetch";


const app = express();
const server = http.createServer(app);
const io = new Server(server);

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);


app.use('/scripts', express.static(path.join(__dirname, 'public')));
app.get("/", function (req, res) {
    const indexPath = path.resolve(__dirname, 'public', 'src', 'index.html');
    res.sendFile(indexPath);
});
app.get("/case/uri_*", (req, res) => {
});


var home = io.of("/");

home.on("connection", function (socket) {
    console.log('a client connected to home');
    socket.on("searchPartyName", function (data) {
        fetchCaseDetails(data, socket);
    });
    socket.on("searchCourtType", function (data) {
        fetchCaseDetails(data, socket);
    });
});

var port = process.env.port || 80;
server.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});

async function fetchCaseDetails(data, socket) {

    var formData = JSON.parse(data);

    var authKey = "Insert JWT Token Here"

    try {

        if (formData.courtTypeCode == "PTY") {

            var clerkUrl = "https://api.browardclerk.org/api/search_party_name.json?person_name=" + formData.value1 + "," + formData.value2 + "&auth_key=" + authKey;
            var myResp = await fetch(clerkUrl);
            var myData = await myResp.json();

            socket.emit("getCaseDetail", JSON.stringify(myData));
        }
        else {

            var clerkUrl = "https://api.browardclerk.org/api/search_cases_filed.json?court_type_code="+ formData.courtTypeCode +"&date_to_use=filed&date="+ formData.value1 +","+ formData.value2 +"&case_type_code=All&auth_key=" + authKey;

            var myResp = await fetch(clerkUrl);
            var myData = await myResp.json();

            socket.emit("getCaseDetail", JSON.stringify(myData));
        }


    } catch (error) {

        console.log(error);

    }

};
