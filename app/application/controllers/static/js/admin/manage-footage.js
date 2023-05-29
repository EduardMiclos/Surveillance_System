$(document).ready(function() {
var footageTable = $('#footage-table').DataTable({
    paging: true,
    lengthChange: false,
    pagingType: 'simple',
    pageLength: 10,
    language: {
    url: '/static/datatables/RO_RO.lang'
    }
});
$('#footage-table tfoot th').each(function() {
    var title = $(this).text();
    $(this).html('<input type="text" placeholder="Search ' + title + '" />');
});

footageTable.columns().every(function() {
    var that = this;
    $('input', this.footer()).on('keyup change', function() {
    if (that.search() == this.value) {
        that.search(this.value).draw();
    }
    });
});
});
