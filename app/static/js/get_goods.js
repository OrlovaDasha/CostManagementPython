$(document).ready(function() {
        var table = $('#goods');

        var goodsTable = table.DataTable({
             serverSide: true,
             searching: false,
             bFilter: false,
             ajax: goods_route,
             columns: [
                {data: "name"},
                {data: "price"},
                 {data:"category"}
                 // {data: "edit"},
                 // {data:"go"}
             ]
            }

        );

    }
);