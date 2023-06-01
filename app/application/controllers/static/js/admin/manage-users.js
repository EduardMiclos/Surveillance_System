$(document).ready(function() {
    $('#users-table').DataTable({
        paging: true,
        lengthChange: false,
        pagingType: 'simple',
        pageLength: 10,
        language: {
        url: '/static/datatables/RO_RO.lang'
        },
})
});
