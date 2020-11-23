
(function($) {

	skel.breakpoints({
		xlarge:	'(max-width: 1680px)',
		large:	'(max-width: 1280px)',
		medium:	'(max-width: 980px)',
		small:	'(max-width: 736px)',
		xsmall:	'(max-width: 480px)'
	});

	$(function() {

		var $window = $(window),
			$body = $('body');

		// Disable animations/transitions until the page has loaded.
			$body.addClass('is-loading');

			$window.on('load', function() {
				window.setTimeout(function() {
					$body.removeClass('is-loading');
				}, 100);
			});

		// Fix: Placeholder polyfill.
			$('form').placeholder();

		// Banner.
			var $banner = $('#banner');

			if ($banner.length > 0) {

				// IE fix.
					if (skel.vars.IEVersion < 12) {

						$window.on('resize', function() {

							var wh = $window.height() * 0.60,
								bh = $banner.height();

							$banner.css('height', 'auto');

							window.setTimeout(function() {

								if (bh < wh)
									$banner.css('height', wh + 'px');

							}, 0);

						});

						$window.on('load', function() {
							$window.triggerHandler('resize');
						});

					}

				// Video check.
					var video = $banner.data('video');

					if (video)
						$window.on('load.banner', function() {

							// Disable banner load event (so it doesn't fire again).
								$window.off('load.banner');

							// Append video if supported.
								if (!skel.vars.mobile
								&&	!skel.breakpoint('large').active
								&&	skel.vars.IEVersion > 9)
									$banner.append('<video autoplay loop><source src="' + video + '.mp4" type="video/mp4" /><source src="' + video + '.webm" type="video/webm" /></video>');

						});

				// More button.
					$banner.find('.more')
						.addClass('scrolly');

			}

		// Scrolly.
			$('.scrolly').scrolly();

	

		// Initial scroll.
			$window.on('load', function() {
				$window.trigger('scroll');
			});

	});

})(jQuery);


let ine = document.getElementById("ine");
let progreso = 0;
ine.addEventListener("click", function(){
    alert("Identificación oficial validada");
    progreso= progreso + 25;
          $("#progress").css("width",progreso+"%");
          $("#progress").text(progreso+"%");
});

let comprobante = document.getElementById("comprobante");
comprobante.addEventListener("click", function(){
    alert("Comprobante de domicilio validado");
    progreso= progreso + 25;
          $("#progress").css("width",progreso+"%");
          $("#progress").text(progreso+"%");
});

let contrato = document.getElementById("contrato");

contrato.addEventListener("click", function(){
    alert("Contrato creado exitosamente");
    progreso= progreso + 25;
          $("#progress").css("width",progreso+"%");
          $("#progress").text(progreso+"%");
});

let email = document.getElementById("email");

email.addEventListener("click", function(){
    alert("Se ha enviado el correo exitosamente");
    progreso= progreso + 25;
          $("#progress").css("width",progreso+"%");
          $("#progress").text(progreso+"%");
});

