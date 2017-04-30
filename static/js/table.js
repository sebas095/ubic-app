$(() => {
    $('.list-btn').click((ev) => {
        $('#data').html('');
        $('.rack-btn').removeClass('icon-color')
        $('.list-btn').addClass('icon-color');
        $('table').css('display', 'block');
    });

    $('.rack-btn').click((ev) => {
        $('.list-btn').removeClass('icon-color');
        $('.rack-btn').addClass('icon-color');
        $('table').css('display', 'none');

        const data = $('tbody').children();
        let content = `<div class="row">`;
        for (let i = 0; i < data.length; i++) {
            if (i % 2 == 0) {
                if (i > 0 || i === data.length - 1) {
                    if (i === data.length - 1 || i === data.length - 2) {
                        content += `</div><div class="row last-rack">`;
                    } else {
                        content += `</div><div class="row">`;
                    }
                } else if (i > 0) {
                    content += `</div>`;
                }
            }

            const td = $(data[i]).children();
            content += '<div class="col-sm-6 view-rack">';
            for (let j = 0; j < td.length; j++) {
                $(td[j]).each(function(index, value) {
                    content += `<p>${$(value).html()}</p>`;
                });
            }
            content += '</div>'
        }
        if (data.length % 2 !== 0) {
            content += '</div>';
        }
        $('#data').html(content);
    });
});