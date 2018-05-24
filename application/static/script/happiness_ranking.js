/* Retrieves a json list of country objects, constructs new table body with the list,
and create|update the happiness_table_body.
The 3 arguments must be checked against the global variables before calling this function.*/
function create_table_body(year, sort_by, ascend) {
    $.ajax({
        url: '/api/happiness_ranking',
        data: {year: year, sort_by: sort_by, ascending: ascend},
        success: function (data) {
            let table_body = '';
            let row_list = [];
            jQuery.each(data, function (index, object) {
                let row = '<tr>';
                let cell_list = [];
                cell_list.push('<td>' + object['Country'] + '</td>');
                cell_list.push('<td>' + object['Happiness Rank'] + '</td>');
                cell_list.push('<td>' + object['Happiness Score'] + '</td>');
                cell_list.push('<td>' + object['Economy GDP per Capita'] + '</td>');
                cell_list.push('<td>' + object['Family'] + '</td>');
                cell_list.push('<td>' + object['Health Life Expectancy'] + '</td>');
                cell_list.push('<td>' + object['Freedom'] + '</td>');
                cell_list.push('<td>' + object['Trust Government Corruption'] + '</td>');
                cell_list.push('<td>' + object['Generosity'] + '</td>');
                cell_list.push('<td>' + object['PM2.5 Air Pollution'] + '</td>');
                jQuery.each(cell_list, function (_index, cell) {
                    row += cell;
                });
                row += '</tr>';
                row_list.push(row);
            });
            jQuery.each(row_list, function (i, _row) {
                table_body += _row;
            });
            $('#happiness_table_body').html(table_body);
        },
        error: function (response) {
            console.log(response)
        }
    });
}


$(document).ready(function () {
    let year = '2016';
    let sort_by = 'Happiness Rank';
    let ascending = '1';

    $('#happiness_table_body').html('<tr><td colspan="10"><h3>Loading Data ..</h3></td></tr>');
    create_table_body(year, sort_by, ascending);

    $('.dropdown_year').click(function () {
        let _year = $(this).val();
        if (_year !== year) {
            year = _year;
            $('#happiness_table_body').prepend('<tr><td colspan="10"><h3>Loading Data ..</h3></td></tr>');
            create_table_body(year, sort_by, ascending);
        }
    });

    $('.dropdown_sort').click(function () {
        let _sort_by = $(this).val();
        if (_sort_by !== sort_by) {
            sort_by = _sort_by;
            create_table_body(year, sort_by, ascending);
        }
    });

    $('.dropdown_ascend').click(function () {
        let _ascending = $(this).val();
        if (_ascending !== ascending) {
            ascending = _ascending;
            $('#dropdown_ascend_button').html($(this).text());
            create_table_body(year, sort_by, ascending);
        }
    });
});
