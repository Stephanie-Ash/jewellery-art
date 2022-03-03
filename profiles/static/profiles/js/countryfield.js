// Set the coulour of the country box based on value selected
let countrySelected = $('#id_default_country').val();
if(!countrySelected) {
    $('#id_default_country').css('color', '#6d7a82');
}
$('#id_default_country').change(function() {
    countrySelected = $(this).val();
    if(!countrySelected) {
        $(this).css('color', '#6d7a82');
    } else {
        $(this).css('color', '#242d33');
    }
});