function validate_set (form) {

    var min = $("#minThre").val()
    var max = $("#maxThre").val()

    min = parseInt(min)
    max = parseInt(max)
    alert(min)
    if (min >= max) {
        alert("Green Sign could not be lower than Red Sign")
        return false
    };
}