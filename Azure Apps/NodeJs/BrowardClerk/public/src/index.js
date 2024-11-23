Date.prototype.toDateInputValue = (function () {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0, 10);
});

var courtCode = "";

$(document).ready(function () {

    $(".btnCaseSearch").click(function (event) {

        event.preventDefault();

        if ($(this).attr("courtCode") == "PTY") {

            $("#section1").hide();
            $("#section2").fadeIn();
            courtCode = "PTY";

        }
        else {
            $("#section1").hide();
            $("#section3").fadeIn();

            courtCode = $(this).attr("courtCode");
            $("#beginFileDate").val(new Date().toDateInputValue());
            $("#endFileDate").val(new Date().toDateInputValue());


        }
    });

    $("#submitDateRange").click(function (event) {

        event.preventDefault();

        $("#loadCaseDetails").children().remove();
        $("#loadCaseDetailsTable").hide();

        var myFormData = {
            "courtTypeCode": courtCode,
            "value1": $("#beginFileDate").val(),  //begin Date
            "value2": $("#endFileDate").val()   //end Date
        };

        console.log(myFormData);

        socket.emit("searchCourtType", JSON.stringify(myFormData));

        socket.on("getCaseDetail", function (data) {
            loadCaseDetails(JSON.parse(data)).then((mainHtml2) => {
                $("#loadCaseDetails").append(mainHtml2);
            }).then(() => {
                $("#section3").hide();
                $("#loadCaseDetailsTable").fadeIn("slow");
            });
        });

    });

    $("#submitPartyName").click(function (event) {

        event.preventDefault();

        $("#loadCaseDetails").children().remove();
        $("#loadCaseDetailsTable").hide();


        var myFormData = {
            "courtTypeCode": courtCode,
            "value1": $("#lname").val(),  //lname
            "value2": $("#fname").val()   //fname
        };


        console.log(myFormData);

        $(this).prop("disabled", true);

        socket.emit("searchPartyName", JSON.stringify(myFormData));

        socket.on("getCaseDetail", function (data) {
            loadPTYCaseDetails(JSON.parse(data)).then((mainHtml) => {
                $("#loadCaseDetails").append(mainHtml);
            }).then(() => {

                $("#section2").hide();
                $("#loadCaseDetailsTable").fadeIn("slow");

            });
        });
    });
});


async function loadPTYCaseDetails(data) {
    return new Promise((resolve) => {
        var myHTML = ``;
        for (var i = 0; i < data.length; i++) {
            var k = data[i];
            var mySelHtml = ``;

            for (var [key, value] of Object.entries(k)) {
                var akey = (`${key}`).toString();
                if (akey.substring(0, 4) == "uri_") {
                    var myKey = akey.split("ri_");
                    mySelHtml += `<option value="${value}">` + myKey[1] + `</option>`;
                }
            }

            myHTML += `<tr id="` + k.Case_Number + `">
                            <td style="color: blue;"><b>`+ k.Case_Number + `</b></td>
                            <td>`+ k.Filed_Date + `</td>
                            <td>`+ k.Party_Type + `</td>
                            <td>`+ k.Party_Last_Name + `, ` + k.Party_First_Name + ` ` + k.Party_Middle_Name + `</td>
                            <td>
                                <select class="form-control form-select thisPartyURI">
                                    <option value="0">select case detail</option>` + mySelHtml + `</select>
                            </td>
                            <td>
                                <button type="button" class="btn btn-outline-success clickViewDisp" data-bs-toggle="modal" data-bs-target="#staticBackdrop">View Case Details</button>  
                            </td>
                        </tr>`;

        }


        resolve(myHTML);

    });

};

async function loadCaseDetails(data) {

    return new Promise((resolve) => {
        var myHTML2 = ``;
        for (var i = 0; i < data.length; i++) {
            var k = data[i];
            var mySelHtml = ``;

            for (var [key, value] of Object.entries(k)) {
                var akey = (`${key}`).toString();
                if (akey.substring(0, 4) == "uri_") {
                    var myKey = akey.split("ri_");
                    mySelHtml += `<option value="${value}">` + myKey[1] + `</option>`;
                }
            }

            myHTML2 += `<tr id="` + k.Case_Number + `">
                            <td style="color: blue;"><b>`+ k.Case_Number + `</b></td>
                            <td>`+ k.Filed_Date + `</td>
                            <td>UNK Party Type</td>
                            <td>`+ k.Caption + `</td>
                            <td>
                                <select class="form-control form-select thisPartyURI">
                                    <option value="0">select case detail</option>` + mySelHtml + `</select>
                            </td>
                            <td>
                                <button type="button" class="btn btn-outline-success clickViewDisp" data-bs-toggle="modal" data-bs-target="#staticBackdrop">View Case Details</button>  
                            </td>
                        </tr>`;

        }


        resolve(myHTML2);

    });

};

