function TikiBar(selector, url) {
    function summon() {
        var container = $('<section>')
            .attr('id', 'tikibar-modal')
            .css('position', 'fixed')
            .css('top', 0)
            .css('right', 0)
            .css('bottom', 0)
            .css('left', 0)
            .css('display', 'none')
            .css('overflow', 'auto')
            .css('z-index', 1000)
            .css('outline', 0)
            .css('background', 'rgba(0, 0, 0, 0.8)')
            .css('box-sizing', 'border-box');
        $('<iframe>')
            .attr('id', 'tikibar')
            .attr('allowtransparency', 'true')
            .attr('src', url)
            .attr('seamless', '')
            .attr('scrolling', 'no')
            .attr('frameborder', 0)
            .css('border', 'none')
            .css('display', 'block')
            .width('100%')
            .appendTo(container);
        container.appendTo('body');
        container.fadeIn(); 
        container.on('click', function(event) {
            event.preventDefault();
            dismiss();
        });
    }

    function dismiss() {
        $('#tikibar-modal').fadeOut().delay(500).remove();
    }

    function set_height(height) {
        $('#tikibar').height(height + 'px');
    }

    $(selector).on('click', summon);

    return {
        dismiss: dismiss,
        set_height: set_height,
        summon: summon
    }
}
