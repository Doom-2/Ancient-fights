$(document).ready(function () {

    $('form').on('submit', function (event) {
        $.ajax({
            url: '/choose-hero/',
            type: 'post',
            dataType: "json",
            data: $('#form-player').serialize(),
            success: [function () {
                window.location.href = '/choose-enemy/'
            }]
        })
        event.preventDefault()
    })

    $('#form-enemy').on('submit', function (event) {
        $.ajax({
            url: '/choose-enemy/',
            type: 'post',
            dataType: "json",
            data: $('#form-enemy').serialize(),
            success: [function () {
                window.location.href = '/fight/'
                // $('#body').html(jQuery(data2).find('#body').html())
                // $("body").load("/choose-enemy/")
            }]
        })
        event.preventDefault()
    })
})
