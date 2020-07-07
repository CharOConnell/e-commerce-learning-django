// collect the country that's initially selected
let countrySelected = $('#id_default_country').val();
// if it's not selected it'll be an empty string
if(!countrySelected) {
    $('#id_default_country').css('color', '#aab7c4');
}
// capture the change event
$('#id_default_country').change(function() {
    countrySelected = $(this).val();
    if(!countrySelected) {
        $(this).css('color', '#aab7c4');
    } else {
        $(this).css('color', '#000');
    }
});