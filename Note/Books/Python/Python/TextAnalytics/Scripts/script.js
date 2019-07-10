$("#btnconnection").on('click',function () {   //$('#button1').one('click', clickHandler)
    var InputValues = {
        Server: $("#server").val(),
        ServerIp: $("#serverip").val(),
        UserName: $("#username").val(),
        Password: $("#password").val(),
        Port: $("#port").val(),
        Database: $("#database").val(),
        SId: $("#sid").val(),
        Query: $("#query").val(),
        Independant: $("#Independant").val(),
        dependant: $("#dependant").val(),
        Variable: $("#Variable").val()
    };

  $.ajax({
        // jQuery:support.cors = true,
        url: "http://127.0.0.1:8090/Connection/",
        contentType: "application/json",
        type: 'POST',   
        data: JSON.stringify(InputValues),
        // data: { name: "John", location: "Boston" },
        success: function (data) {
           
            setTimeout(function(){             
            
            $('#myDiv1').fadeOut('fast');
            var realjson = JSON.parse(data);

            var tableHolder = "<table class='table'>";
            tableHolder += "<tr><th>Accuracy</th><th>Sensitivity</th><th>False Positive Rate</th><th>Specificity</th><th>Miss-Classification Error</th><th>F1 Score</th><th>Threshold Probability Value</th></tr>";
            realjson.forEach(function (data, index) {
                tableHolder += "<tr><td>" + data.Accuracy + "</td><td>" + data.Sensitivity + "</td><td>" + data.FalsePositiveRate + "</td><td>" + data.Specificity + "</td><td>" + data.Mis_Class_Error + "</td><td>" + data.F1Score + "</td><td>" + data.Thresholds + "</td></tr>";  
            });
            tableHolder += "</table>";

            $("#AlgorithmTable").html(tableHolder);}, 5000);
            // var realjson = JSON.parse(data);

            // var tableHolder = "<table class='table'>";
            // tableHolder += "<tr><th>Accuracy</th><th>Sensitivity</th><th>False Positive Rate</th><th>Specificity</th><th>Miss-Classification Error</th><th>F1 Score</th><th>Threshold Probability Value</th></tr>";
            // realjson.forEach(function (data, index) {
            //     tableHolder += "<tr><td>" + data.Accuracy + "</td><td>" + data.Sensitivity + "</td><td>" + data.FalsePositiveRate + "</td><td>" + data.Specificity + "</td><td>" + data.Mis_Class_Error + "</td><td>" + data.F1Score + "</td><td>" + data.Thresholds + "</td></tr>";  
            // });
            // tableHolder += "</table>";

            // $("#AlgorithmTable").html(tableHolder);

        },
        error: function (e) {
            console.log(e);
        }
    })
    $.ajax({
        // jQuery:support.cors = true,
        url: "http://127.0.0.1:8090/Scoring/",
        contentType: "application/json",
        type: 'POST',
        data: JSON.stringify(InputValues),
        // data: { name: "John", location: "Boston" },
        success: function (data) {
            console.log(typeof data);
            
            setTimeout(function()
        {             
 
            $('#myDiv').fadeOut('fast');
            var realjson = JSON.parse(data);

            var tableHolder = "<table class='table'>";
            tableHolder += "<tr><th>Comment_Index</th><th>Comments</th><th>Predicted</th><th>Probability_1</th><th>Probability_0</th></tr>";
            realjson.forEach(function (data, index) {
                tableHolder += "<tr><td>" + data.Comment_Index + "</td><td>" + data.Comments + "</td><td>" + data.Predicted + "</td><td>" + data.Probability_1 + "</td><td>" + data.Probability_0 + "</td></tr>";
            });
            tableHolder += "</table>";

            $("#Scoring").html(tableHolder); 
        }, 20000);

            // var realjson = JSON.parse(data);

            // var tableHolder = "<table class='table'>";
            // tableHolder += "<tr><th>Comment_Index</th><th>Comments</th><th>Predicted</th><th>Probability_1</th><th>Probability_0</th></tr>";
            // realjson.forEach(function (data, index) {
            //     tableHolder += "<tr><td>" + data.Comment_Index + "</td><td>" + data.Comments + "</td><td>" + data.Predicted + "</td><td>" + data.Probability_1 + "</td><td>" + data.Probability_0 + "</td></tr>";
            // });
            // tableHolder += "</table>";

            // $("#Scoring").html(tableHolder);

        },
        error: function (e) {
            console.log(e);
        }
    })
})
      


// document.getElementById("Algorithm").onload = function () { myFunction() };
// function myFunction() {
//     $.ajax({
//         // jQuery:support.cors = true,
//         url: "http://127.0.0.1:8090/training/",
//         type: 'GET',
//         success: function (data) {
//             console.log(data)

//         },
//         error: function (e) {
//             console.log(e);
//         }
//     })
// }



// Url call
//$.post( "/project/test/auto", data );






