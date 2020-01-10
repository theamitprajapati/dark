var validateCheckRadio = function (val) {
    $("input[type='radio'], input[type='checkbox']").on('ifChecked', function (event) {
        $(this).parent().closest(".has-error").removeClass("has-error").addClass("has-success").find(".help-block").hide().end().find('.symbol').addClass('ok');
    });
};
var viewFormValues = function () {

    if ($('input[class="featuredlist"]')) {
        $('p[data-display="featuredlist"]').html($('.featuredlist:checked').map(function () { return ($(this).parent().text()).trim(); }).get().join(', '))
    }
    for (var i = 1; i <= 4; i++) {
        if ($('input[class="features_list' + i + '"]')) {
            $('p[data-display="features_list' + i + '"]').html($('.features_list' + i + ':checked').map(function () { return ($(this).parent().parent().text()).trim(); }).get().join(', '))
        }
    }


    $('.display-value', form).each(function () {
        var input = $('[name="' + $(this).attr("data-display") + '"]', form);
        if (input.attr("type") == "text" || input.attr("type") == "email" || input.attr("type") == "number" || input.is("textarea")) {
            $(this).html(input.val());
        } else if (input.is("select")) {
            $(this).html(input.find('option:selected').text());
        } else if (input.is(":radio") || input.is(":checkbox")) {
            $(this).html(input.filter(":checked").closest('label').text());
        } else if ($(this).attr("data-display") == 'card_expiry') {
            $(this).html($('[name="card_expiry_mm"]', form).val() + '/' + $('[name="card_expiry_yyyy"]', form).val());
        }
    });
};


// function to initiate Validation Sample 1
var setValidator = function (element, rules, message = '', group = '', isModel = '0') {

    var form1 = $(element);
    var errorHandler1 = $('.errorHandler', form1);
    var successHandler1 = $('.successHandler', form1);
    $.validator.addMethod("FullDate", function () {
        //if all values are selected
        if ($("#dd").val() != "" && $("#mm").val() != "" && $("#yyyy").val() != "") {
            return true;
        } else {
            return false;
        }
    }, 'Please select a day, month, and year');
    $.validator.addMethod("words", function (value, element) {
        return this.optional(element) || /^[a-zA-Z ]*$/.test(value);
    }, "Invalid name");
    $.validator.addMethod(
        "regex",
        function (value, element, regexp) {
            var re = new RegExp(regexp);
            return this.optional(element) || re.test(value);
        },
        "Invalid format."
    );
    $(element).validate({
        errorElement: "span", // contain the error msg in a span tag
        errorClass: 'help-block',
        errorPlacement: function (error, element) { // render error placement for each input type
            if (element.attr("type") == "radio" || element.attr("type") == "checkbox") { // for chosen elements, need to insert the error after the chosen container
                error.insertAfter($(element).closest('.form-group').children('div').children().last());
            } else if (element.attr("name") == "dd" || element.attr("name") == "mm" || element.attr("name") == "yyyy") {
                error.insertAfter($(element).closest('.form-group').children('div'));
            } else {
                error.insertAfter(element);
                // for other inputs, just perform default behavior
            }
        },
        ignore: ":hidden",
        rules: rules,
        messages: message,
        groups: group,
        invalidHandler: function (event, validator) { //display error alert on form submit
            successHandler1.hide();
            errorHandler1.show();

        },
        highlight: function (element) {
            $(element).closest('.help-block').removeClass('valid');
            // display OK icon
            $(element).closest('.form-group').removeClass('has-success').addClass('has-error').find('.symbol').removeClass('ok').addClass('required');
            // add the Bootstrap error class to the control group
        },
        unhighlight: function (element) { // revert the change done by hightlight
            $(element).closest('.form-group').removeClass('has-error');
            // set error class to the control group
        },
        success: function (label, element) {
            label.addClass('help-block valid');
            // mark the current input as valid and display OK icon
            $(element).closest('.form-group').removeClass('has-error').addClass('has-success').find('.symbol').removeClass('required').addClass('ok');
        },
        submitHandler: function (form) {
            if (isModel == 1) {
                var status = $('#myModal').modal('show').on('click', '#submit-confirmation', function (e) {
                    $('#myModal').modal('hide');

                    return form.submit();
                });
            } else {
                return form.submit();
            }
            //    console.log(status);
            //     if (confirm('Are you sure want to submit ?')) {

            //     }
        }
    });
};

// function to initiate Validation Sample 2