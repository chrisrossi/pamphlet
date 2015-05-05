var tikibar = function() {
    function add_instance(anchor) {
        var ct = $(anchor).data('content-type');
        var url = '@@tikibar-add-instance?content_type=' + escape(ct);
        new_tab('Add ' + ct, url);
    }

    function new_tab(title, url) {
        var id = 'tab-' + ($('#tikibar-tabs li').length + 1);
        var tab = $('<li>').attr('role', 'presentation')
            .append($('<a>')
                        .attr('href', '#' + id)
                        .attr('aria-controls', 'add-instance')
                        .attr('role', 'tab')
                        .attr('data-toggle', 'tab')
                        .text(title))
            .appendTo($('#tikibar-tabs'));

        $.get(url, function(data) {
            var pane = $('<div>').attr('role', 'tabpanel')
                .attr('class', 'tab-pane')
                .attr('id', id)
                .html(data)
                .appendTo($('#tikibar-panels'));
            tab.find('a').click();
            pane.find('form')
                .attr('action', url)
                .on('submit', function(event) {
                    event.preventDefault();
                    $.ajax({
                        url: url, 
                        data: $(this).serialize(), 
                        method: 'POST',
                        success: function(href) {
                            parent.location.href = href;
                        }
                    });
                });
        });
    }

    $(document).ready(function(event) {
        // Set height of iframe
        if (parent !== window)
            parent.tikibar.set_height(document.body.scrollHeight);

        // Handle dismiss button
        $('.close').on('click', function(event) {
          event.preventDefault();
          parent.tikibar.dismiss();
        });

        // Handle add-instance
        $('.add-instance').on('click', function(event) {
            event.preventDefault();
            add_instance(this);
        });
    });

    return {
        new_tab: new_tab
    };
}();
