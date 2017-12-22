$(function () {
    $('.content-separator input').on('keyup', function (e) {
        var button = e.which;

        if (button < 32 && button !== 8) {
            return false;
        }

        var terms = $('.term');
        var value = $(this).val();

        $('.letters-buttons button').removeClass('selected-button');
        $('.letters-buttons button[data--letter=ALL]').addClass('selected-button');
        $('.category-buttons button').removeClass('selected-button');

        if (!value) return terms.show();

        $.each(terms, function () {
            var name = $(this).data('Name');

            if (!name.includes(value)) return $(this).hide();

            $(this).show()
        });
    });

    $('.letters-buttons button').on('click', function () {
        var letter = $(this).data('Letter');
        var terms = $('.term');

        $('.content-separator input').val('');
        $('.category-buttons button').removeClass('selected-button');
        $('.letters-buttons button').removeClass('selected-button');

        $(this).addClass('selected-button');

        if (letter === 'ALL') return terms.show();

        terms.hide();

        $('.term[data--letter=' + letter + ']').show();
    });

    $('.category-buttons button').on('click', function () {
        var category = $(this).data('Category');
        var terms = $('.term');

        $('.content-separator input').val('');
        $('.category-buttons button').removeClass('selected-button');
        $('.letters-buttons button').removeClass('selected-button');
        $('.letters-buttons button[data--letter=ALL]').addClass('selected-button');

        $(this).addClass('selected-button');

        terms.hide();

        $('.term[data--category=' + category + ']').show();
    });
});