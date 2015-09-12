function validate (form) {
    var input = $("#bugid").val()
    var id = parseInt(input)
    if (isNaN(id)) {
        alert("Invalid BugID!")
        return false
    } else {
        return true
    }
}