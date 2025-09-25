/////**
//// * @license Copyright (c) 2003-2023, CKSource Holding sp. z o.o. All rights reserved.
//// * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
//// */
////
////CKEDITOR.editorConfig = function( config ) {
////	// Define changes to default configuration here. For example:
////	// config.language = 'fr';
////	// config.uiColor = '#AADC6E';
////};
//CKEDITOR.editorConfig = function(config) {
//    // Добавляем кастомные стили для контента внутри редактора
//    config.contentsCss = [
//        // Путь к твоему кастомному CSS (если есть)
//        // config.contentsCss.push(CKEDITOR.basePath + 'contents.css');
//        // Или добавляем стили напрямую
//    ];
//
//    // Дополнительно: Настройка для вставки видео/iframe
//    config.extraAllowedContent = 'video[*]{*} iframe[*]{*}'; // Разрешаем атрибуты для видео и iframe
//
//    // Обработчик для применения стилей после вставки
//    config.on = {
//        'instanceReady': function(ev) {
//            const editor = ev.editor;
//            // Функция для видео и iframe
//            function setMediaAttributes() {
//                // Для видео
//                const videos = editor.document.getElementsByTag('video');
//                for (let video of videos) {
//                    video.setAttribute('width', '100%');
//                    video.setAttribute('height', 'auto');
//                    video.setAttribute('style', 'max-width: 100% !important; width: 100% !important; height: auto !important;');
//                }
//                // Для iframe (как в предыдущем коде)
//                const iframes = editor.document.getElementsByTag('iframe');
//                for (let iframe of iframes) {
//                    iframe.setAttribute('width', '100%');
//                    iframe.setAttribute('height', 'auto');
//                    iframe.setAttribute('style', 'max-width: 100% !important; width: 100% !important; height: auto !important;');
//                }
//            }
//            setMediaAttributes();
//
//            // При вставке/изменении
//            editor.on('afterPaste', function() {
//                setTimeout(() => setMediaAttributes(), 50);
//            });
//            editor.on('change', function() {
//                setTimeout(() => setMediaAttributes(), 100);
//            });
//            // Для видео: После загрузки (через setTimeout)
//            setTimeout(() => setMediaAttributes(), 1000);
//        }
//    };
//};
/**
 * @license Copyright (c) 2003-2023, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
};