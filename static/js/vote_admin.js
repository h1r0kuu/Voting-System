// static/js/vote_admin.js
window.addEventListener("load", function() {

(function($) {
    $(document).ready(function() {
        var votingField = $("#id_voting");
        var optionField = $("#id_option");

        function updateOptions() {
            var selectedVoting = votingField.val();
            if (selectedVoting) {
                $.ajax({
                    url: optionsUrl,
                    data: { voting_id: selectedVoting },
                    dataType: 'json',
                    success: function(data) {
                        optionField.empty();
                        $.each(data.options, function(index, option) {
                            optionField.append('<option value="' + option.id + '">' + option.option_value + '</option>');
                        });
                    }
                });
            }
        }

        updateOptions();

        votingField.change(updateOptions);
    });
})(django.jQuery);
})