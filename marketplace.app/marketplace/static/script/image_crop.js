// ===== Get photo_url =====
    if (($('#createProductPage').length > 0) || ($('#editProducerForm').length > 0) || ($('#editProductForm').length > 0))  {
        var photo_url,
            type,
            viewportHeight,
            imageWidth,
            imageHeight;
// see if a product or producer is being edited/created
        var addr = window.location + '';
        addr = addr.split('/');

        function setSrcAttr(type) {
            $.get('/api/v1/' + type + '/' + id, function (data) {
                $(".gambar").attr("src", '/' + data.photo_url);
            })
        }

        if ((addr[3] === 'producer') && (addr[5] === 'edit')) {
            var id = addr[4];
            var type = 'producers';
            viewportHeight = 64;
            imageWidth = 1000;
            imageHeight = 324;
            setSrcAttr(type);
        }
        else if ((addr[3] === 'producer') && (addr[5] === 'products')) {
            var id = addr[6];
            var type = 'products';
            viewportHeight = 150;
            imageWidth = 1020;
            imageHeight = 764;
            setSrcAttr(type);
        }

        else if ((addr[3] === 'producer') && (addr[5] === 'create_product')) {
            var type = 'products';
            viewportHeight = 150;
            imageWidth = 1020;
            imageHeight = 764;
            $(".gambar").attr("src", '/static/img/standard.png');
        }

        var $uploadCrop,
            tempFilename,
            rawImg,
            imageId;

        function readFile(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    $('.upload-demo').addClass('ready');
                    $('#cropImagePop').modal('show');
                    rawImg = e.target.result;
                };
                reader.readAsDataURL(input.files[0]);
            }
            else {
                swal("Sorry - you're browser doesn't support the FileReader API");
            }
        }

        $uploadCrop = $('#upload-demo').croppie({
            viewport: {
                width: 200,
                height: viewportHeight,
            },
            enforceBoundary: false,
            enableExif: true
        });


        $('#cropImagePop').on('shown.bs.modal', function () {
            $uploadCrop.croppie('bind', {
                url: rawImg
            }).then(function () {
                console.log('jQuery bind complete');
            });
        });

        $('.item-img').on('change', function () {
            imageId = $(this).data('id');
            tempFilename = $(this).val();
            $('#cancelCropBtn').data('id', imageId);
            readFile(this);
        });
        $('#cropImageBtn').on('click', function (ev) {
            $uploadCrop.croppie('result', {
                type: 'base64',
                format: 'jpeg',
                size: {width: imageWidth, height: imageHeight}
            }).then(function (resp) {
                $('#item-img-output').attr('src', resp);
                $('#cropImagePop').modal('hide');
            });
        });
    }
// End upload preview image
