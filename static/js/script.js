// Toast launch
$('.toast').toast('show');

// Modal launch
$('.delete-btn').click(function () {
    let del_url = $(this).data('delete-url');
    console.log(del_url)
    if (del_url.includes('review')) {
        $('#review-delete').attr('href', del_url);
        $('#review-delete-modal').modal();
    } else if (del_url.includes('designer')) {
        $('#designer-delete').attr('href', del_url);
        $('#designer-delete-modal').modal();
    } else if (del_url.includes('product')) {
        $('#product-delete').attr('href', del_url);
        $('#product-delete-modal').modal();
    } else if (del_url.includes('faq')) {
        $('#faq-delete').attr('href', del_url);
        $('#faq-delete-modal').modal();
    }
})