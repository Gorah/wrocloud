function metadata(URL) {
    console.log(URL);
}

function newdirectory() {
    $("#create_new_dir").modal();
}

function createdirectory() {
    $.ajax({
        type: "POST",
        url: "/create_directory/",
        data: {
            directory: CONFIG.PATH + $("#directory-name-text").val()
        },
        success: function(data, textStatus, jqXHR) {
            createddirectory();
        }
    });
}

function createddirectory() {
    location.reload();
}

function setcookieandsubmit() {
    $.cookie("lastfile", $("#filename").val(), {path: "/"});
    console.log($("#filename").val());
    console.log($("#fileupload").submit());
}
