$(document).ready(function () {
    $('.btn-success').click(function () {
        $.ajax({
            url: '/fight/hit',
            type: 'get',
            dataType: 'html',
            success: [function (data) {
                $('.battle-stat').html(jQuery(data).find('.battle-stat').html())
                $('.self-health-stamina').html(jQuery(data).find('.self-health-stamina').html())
                $('.enemy-health-stamina').html(jQuery(data).find('.enemy-health-stamina').html())
                $('.battle-result').html(jQuery(data).find('.battle-result').html())

            }]
        })
    })
    $('.btn-danger').click(function () {
        $.ajax({
            url: '/fight/use-skill',
            type: 'get',
            dataType: 'html',
            success: [function (data2) {
                $('.battle-stat').html(jQuery(data2).find('.battle-stat').html())
                $('.self-health-stamina').html(jQuery(data2).find('.self-health-stamina').html())
                $('.enemy-health-stamina').html(jQuery(data2).find('.enemy-health-stamina').html())
                $('.battle-result').html(jQuery(data2).find('.battle-result').html())

            }]
        })
    })
    $('.btn-warning').click(function () {
        $.ajax({
            url: '/fight/pass-turn',
            type: 'get',
            dataType: 'html',
            contentType: "text/html",
            success: [function (data3) {
                $('.battle-stat').html(jQuery(data3).find('.battle-stat').html())
                $('.self-health-stamina').html(jQuery(data3).find('.self-health-stamina').html())
                $('.enemy-health-stamina').html(jQuery(data3).find('.enemy-health-stamina').html())
                $('.battle-result').html(jQuery(data3).find('.battle-result').html())
            }]
        })
    })
})
