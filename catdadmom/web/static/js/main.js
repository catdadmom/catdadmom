//var container = document.getElementById('map'); //지도를 담을 영역의 DOM 레퍼런스
//var options = { //지도를 생성할 때 필요한 기본 옵션
//    center: new daum.maps.LatLng(37.485659, 127.004036), //지도의 중심좌표.
//    level: 3 //지도의 레벨(확대, 축소 정도)
//};
//
//var map = new daum.maps.Map(container, options); //지도 생성 및 객체 리턴


$(function () {
    function s3_upload() {
        var $status = $('#status');
        var $preview = $('#preview');

        new S3Upload({
            file_dom_selector: 'files',
            s3_sign_put_url: '/sign_s3/',
            onProgress: function (percent, message) {
                $status.text('Upload progress: ' + percent + '% ' + message);
            },
            onFinishS3Put: function (url) {
                $preview.html('<img src="' + url + '">');
            },
            onError: function (status) {
                $status.text('Upload error: ' + status);
            }
        });
    }

    $('#files').on('change', s3_upload);
});