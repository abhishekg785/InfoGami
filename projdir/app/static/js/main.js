var visualDiv = $('#visualDiv'),
    closeMusic = $('#closeMusic'),
		musicName = $('#musicName h1'),
		musicVisual = $('#musicVisual'),
		is_playing = false,
    old_track = "",
		new_track = "",
		//parameters for the svg visual data animation
		svgHeight = 300,
		svgWidth = 1200,
		barPadding = 1,
		frequencyData = new Uint8Array(200);



function playMusic(music_id,music_name){

	var track_id = 'music' + music_id;
	musicName.html(music_name);

	visualDiv.css('display','block')
	if(is_playing == false){
	  new_track = $("#"+track_id)[0];
		old_track = new_track;
	  is_playing = true;
	  new_track.play();
  }
	else if(is_playing == true){
		new_track = $("#"+track_id)[0];
    old_track.pause();
		old_track.currentTime = 0;
		new_track.play();
		old_track = new_track;
	}


	var graph = createSVG('#musicVisual',svgHeight,svgWidth);
	graph.selectAll('rect')
	  .data(frequencyData)
		.enter()
		.append('rect')
		.attr('width',svgWidth / frequencyData.length - barPadding)
		.attr('x',function(d,i){
			return i*(svgWidth / frequencyData.length);
		});


	var audioCtx = new (window.AudioContext || window.webkitAudioContext)(),
	    audioSrc = audioCtx.createMediaElementSource(new_track),
	    analyser = audioCtx.createAnalyser();
			audioSrc.connect(analyser);
	    audioSrc.connect(audioCtx.destination);

			function renderChart(){
				requestAnimationFrame(renderChart);

				//copy frequencydata to frequencydataArray
				analyser.getByteFrequencyData(frequencyData);

				//update d3 chart with new data
				graph.selectAll('rect')
					.data(frequencyData)
					.attr('y',function(d){
						return svgHeight - d;
					})
					.attr('height',function(d){
						return d;
					})
					.attr('fill',function(d){
						return 'rgb(0,0,' +d +')';
					});
			}
	renderChart();
}


	$('#closeMusic').on('click',function(){
		visualDiv.css('display','none');
		new_track.pause();
		new_track.currentTime = 0;
	});


function createSVG(parent,height,width){
	return d3.select(parent).append('svg').attr('height',height).attr('width',width)
}



(function($) {
	skel.breakpoints({
		xlarge:	'(max-width: 1680px)',
		large:	'(max-width: 1280px)',
		medium:	'(max-width: 980px)',
		small:	'(max-width: 736px)',
		xsmall:	'(max-width: 480px)'
	});

	$(function() {
		var	$window = $(window),
			$body = $('body'),
			$menu = $('#menu'),
			$sidebar = $('#sidebar'),
			$main = $('#main');
			$loader = $('#loader')

		// Disable animations/transitions until the page has loaded.
			$body.addClass('is-loading');

			$window.on('load', function() {
				window.setTimeout(function() {
					$body.removeClass('is-loading');
				}, 100);
			});

		// Fix: Placeholder polyfill.
			$('form').placeholder();

		// Prioritize "important" elements on medium.
			skel.on('+medium -medium', function() {
				$.prioritize(
					'.important\\28 medium\\29',
					skel.breakpoint('medium').active
				);
			});

		// IE<=9: Reverse order of main and sidebar.
			if (skel.vars.IEVersion <= 9)
				$main.insertAfter($sidebar);

		// Menu.
			$menu
				.appendTo($body)
				.panel({
					delay: 500,
					hideOnClick: true,
					hideOnSwipe: true,
					resetScroll: true,
					resetForms: true,
					side: 'right',
					target: $body,
					visibleClass: 'is-menu-visible'
				});

		// Search (header).
			var $search = $('#search'),
				$search_input = $search.find('input');

			$body
				.on('click', '[href="#search"]', function(event) {

					event.preventDefault();

					// Not visible?
						if (!$search.hasClass('visible')) {

							// Reset form.
								$search[0].reset();

							// Show.
								$search.addClass('visible');

							// Focus input.
								$search_input.focus();

						}

				});

			$search_input
				.on('keydown', function(event) {

					if (event.keyCode == 27)
						$search_input.blur();

				})
				.on('blur', function() {
					window.setTimeout(function() {
						$search.removeClass('visible');
					}, 100);
				});

		// Intro.
			var $intro = $('#intro');

			// Move to main on <=large, back to sidebar on >large.
				skel
					.on('+large', function() {
						$intro.prependTo($main);
					})
					.on('-large', function() {
						$intro.prependTo($sidebar);
					});

	});
})(jQuery);
