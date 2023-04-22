let container = " <div class=\"col-5\">\n" +
    "                        <table class=\"table\">\n" +
    "                            <thead class=\"table-dark\">\n" +
    "                            <tr>\n" +
    "                                <th scope=\"col\">Nom d'établissement</th>\n" +
    "                                <th scope=\"col\">Nombre de constats</th>\n" +
    "                            </tr>\n" +
    "                            </thead>\n" +
    "                            <tbody id=\"tbody\">\n" +
    "                            </tbody>\n" +
    "                        </table>\n" +
    "                    </div>";

let modal_container = "    <div class=\"row table-responsive\">\n" +
    "            <table class=\"table\">\n" +
    "                <thead class=\"table-dark\">\n" +
    "                <tr>\n" +
    "                    <th scope=\"col\">date_constat</th>\n" +
    "                    <th scope=\"col\">adresse</th>\n" +
    "                    <th scope=\"col\">date_jugement</th>\n" +
    "                    <th scope=\"col\">etablissement</th>\n" +
    "                    <th scope=\"col\">montant</th>\n" +
    "                    <th scope=\"col\">proprietaire</th>\n" +
    "                    <th scope=\"col\">ville</th>\n" +
    "                    <th scope=\"col\">status</th>\n" +
    "                    <th scope=\"col\">date_status</th>\n" +
    "                    <th scope=\"col\">categorie</th>\n" +
    "                    <th>&nbsp;</th>\n" +
    "                <tbody id=\"modaltbody\">" +
    "               </tbody>\n" +
    "            </table>\n" +
    "        </div>"

// recherche par date
$(document).ready(function () {
    $("#formajax").submit(function (event) {
        let formData = {
            du: $("#du").val(),
            au: $("#au").val(),

        };
        console.log(formData);
        $.ajax({
            type: "GET",
            url: "/api/contrevenants",
            data: formData,
            success: function (response) {
                const parsedData = JSON.parse(response);
                const liste = {};

                parsedData.forEach(violation => {
                if (!liste[violation.etablissement]) { //check occurence. si non initialise a 0
                 liste[violation.etablissement] = 0;
                }

                liste[violation.etablissement]++; // si oui, incremente le nombre de constat pour cet etablissement
                });
                $("#resultats").html(container);
                let tbody = $("#tbody");
                for (const etablissement in liste) {
                    tbody.append("<tr>" +
                        "<td>" + etablissement + "</td>" +
                        "<td>" + liste[etablissement] + "</td></tr>");
                }
            },
            error: function (xhr) {
                alert("error : " + xhr);
            }
        });
        event.preventDefault();
    });
});
// AJAX requete pour l'auto completion
$(document).ready(function () {
    $("#searchbox").keyup(function () {
        let suggestion_box = $("#suggesstion-box");
        $.ajax({
            type: "POST",
            url: "/autocomplete",
            data: {'keyword': $("#searchbox").val()},

            success: function (data) {
                let parsedData = JSON.parse(data);
                console.log(parsedData);
                suggestion_box.show();

                $("#ul").empty();
                for (let k in parsedData) {
                    $("#ul").append
                    ("<li onclick=\"selectValue('" + parsedData[k].etablissement + "')\">" + parsedData[k].etablissement +
                        "</li>")
                }
                $("#search-box").css("background", "#FFF");
            }
        });
    });
});

function selectValue(val) {
    $("#searchbox").val(val);
}
//recherche sur le navbar
$(document).ready(function () {
    $("#navsearch").submit(function (event) {
        $.ajax({
            type: "POST",
            url: "api/etablissement",
            data: {'nom': $("#searchbox").val()},
            success: function (response) {
                $('#exampleModal').modal('show');
                const parsedData = JSON.parse(response);
                 $('#exampleModalLabel').text("Résultat de la recherche pour l'établissement : "+parsedData[0].etablissement);
                 $(".modal-body").html(modal_container);
                let tbody = $("#modaltbody");
                    tbody.empty();
                for (var k in parsedData) {
                    tbody.append("<tr style=\"cursor: pointer;\" data-bs-toggle=\"collapse\" " +
                        "data-bs-target=\"#collapse"+ parsedData[k].id_poursuite +"\"\n" +
                        "    aria-expanded=\"false\" aria-controls=\"collapse"+ parsedData[k].id_poursuite +"\">" +
                        "<td>" + parsedData[k].date + "</td>" +
                        "<td>" + parsedData[k].adresse + "</td>" +
                        "<td>" + parsedData[k].date_jugement + "</td>" +
                        "<td>" + parsedData[k].etablissement + "</td>" +
                        "<td>" + parsedData[k].montant + "$</td>" +
                        "<td>" + parsedData[k].proprietaire + "</td>" +
                        "<td>" + parsedData[k].ville + "</td>" +
                        "<td>" + parsedData[k].status + "</td>" +
                        "<td>" + parsedData[k].date_status + "</td>" +
                        "<td>" + parsedData[k].categorie + "</td></tr>"+
                        " <tr> <td colspan=\"20\" class=\"collapse\" id=\"collapse"+ parsedData[k].id_poursuite +"\">"+
                        " " + parsedData[k].description+ "</td></tr>");
                }
            },
            error: function (xhr) {
               console.log(xhr)
            }
        });
        event.preventDefault();
    });
});