function markdownToHTML(text) {
    let converter = new showdown.Converter();
    return converter.makeHtml(text);
}

$(document).ready(function () {
    if ($("#mainProducerDescription").length > 0) {
    let producerDescription = $("#mainProducerDescription");
        let text = producerDescription.attr('data-description');
        text = markdownToHTML(text);
        producerDescription.append(
            text
        );
    }
});
