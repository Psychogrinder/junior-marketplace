function markdownToHTML(text) {
    let converter = new showdown.Converter();
    return converter.makeHtml(text);
}

$(document).ready(function () {
    let producerDescription = $("#mainProducerDescription");
    if (producerDescription.length > 0) {
        let text = producerDescription.attr('data-description');
        text = markdownToHTML(text);
        producerDescription.append(
            text
        );
    }
});