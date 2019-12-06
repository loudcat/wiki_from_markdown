    $.each(JSON.parse(sessionStorage.getItem('menu')), function(index, val) {
        console.log(index)
        if (val){
            $($('.accord').find('.sub')[index]).show()
        }
    })



    function *gens(elems) {
        for(elem of elems) {
            yield $(elem).is(':visible')
        }
    }

    // Menu
    $('.dir').children('a').click(function(e){
        e.preventDefault();
        $(this).parent().children('ul').toggle();
        console.log('a');
        sessionStorage.setItem('menu', JSON.stringify([...gens($('.accord').find('.sub'))]))

    });
    // Search
    $('#search').blur(function() {
        $('#drop').hide('slow');
    });
    $('#search').keyup(function(){
        console.log('search');
        if ($(this).val().length > 2){
            axios.get('/search', {
                params: {
                    q: $(this).val(),
                }
            })
            .then(function (response) {
                $('#drop').empty();
                console.log(response.data);
                var data = response.data.data
                for (file of data){
                    let elem = $('<div>', {}).appendTo('#drop');
                    let name = $('<h5>', {
                    }).append($('<a>', {
                            href: file.href,
                            html: file.file
                    })).appendTo(elem)
                    for (line of file.lines) {
                        $('<p>', {
                            html: line
                        }).append(
                            $('<p>', {
                                text: '...'
                            })
                        ).appendTo(elem)
                    }
                    $('<hr>').appendTo(elem)
                }
                $('<p>', {
                    text: `time: ${response.data.time}`
                }).appendTo('#drop')
                $('#drop').show('slow')
            })
            .catch(function (error) {
                console.log(error);
            })
            .then(function () {
                // always executed
            });
        } else {
             if ($('#drop').is(':visible')) {
                $('#drop').hide('slow')
             }
            $('#drop').empty();

        }

    });