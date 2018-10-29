
$(document).ready(function () {
    $('.page_loader').show();
    get_new_items(0);
});
var itemId = 0;
pages = true;
$(window).scroll(function () {
    if ($(window).scrollTop() + $(window).height() > $(document).height() - 20) {
        console.log("itemId : "+itemId);
        $('.page_loader').show();
        if(pages){
            get_new_items(itemId + 1)
        } else {
            $('.page_loader').hide();
        }
    }
});

function get_new_items(id) {
    var first = id;
    var last  =   id + 25;
    const link = 'https://supplyai-test.herokuapp.com/api/v1/bouncer/products/' + first + '/' + last;
    console.log(link);
    fetch( link)
        .then(response => response.json())
        .then(json => {
            renderItems(json);
        })
}


function renderItems(data){
    var count = Object.keys(data).length;
    if (count < 25){
        pages = false;
    }
    jQuery.each(data, function (i, product) {
        itemId = itemId + 1;
        let created = product.created;
        let image_url = product.image_url;
        let modified = product.modified;
        let price = product.price;
        let product_url = product.product_url;
        let title = product.title;
        const cards = $('#cards-holder');
        let card = `
            <div class="column is-4">
                <div class="card">
                    <div class="card-image">
                        <figure class="image is-4by3">
                            <img src="${image_url}" alt="Placeholder image">
                            </figure>
                        </div>
                        <div class="card-content">
                            <div class="media">
                                <div class="media-content">
                                    <p class="title is-4">${title}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        cards.append(card);
    });
    $('.page_loader').hide();
}