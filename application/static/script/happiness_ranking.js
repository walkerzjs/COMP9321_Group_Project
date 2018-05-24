/* Retrieves a json list of country objects, constructs new table body with the list,
and returns the new table body as html string.
The 3 arguments must be checked against the global variables before calling this function.*/
function create_table_body(year, sort_by, ascend) {
    let table_body = '';
    $.ajax({
        url: '/api/happiness_ranking',
        data: {year: year, sort_by: sort_by, ascending: ascend},
        success: function (data) {
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
            console.log('In ajax success function.');
            console.log(table_body);
        },
        error: function (response) {
            console.log(response)
        }
    });
    console.log('In create table body function');
    console.log(table_body);
    return table_body;
}


$(document).ready(function () {
    let year = 2016;
    let sort_by = 'Happiness Rank';
    let ascending = '1';
    let tbody_object = $('#happiness_table_body');
    tbody_object.html('<tr><td colspan="10"><h3>Loading Data ..</h3></td></tr>');
    let result = create_table_body(year, sort_by, ascending);
    console.log('In main jquery function.');
    console.log(result);
    tbody_object.html(result);

});