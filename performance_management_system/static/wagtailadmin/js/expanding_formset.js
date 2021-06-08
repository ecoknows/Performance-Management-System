// Wagtail 2.8 issue (https://github.com/wagtail/wagtail/issues/5770)
// Nested inline panel fails in saving due to generating wrong names/IDs of input fields
// - we provide a fix working in our situation but not verified against wagtail source code
// - fix implies modification/addition of 2 lines of code (see comments below)


function buildExpandingFormset(prefix, opts) {

	if (!opts) {
		opts = {};
	}
  
	var addButton = $('#' + prefix + '-ADD');
	var formContainer = $('#' + prefix + '-FORMS');
	var totalFormsInput = $('#' + prefix + '-TOTAL_FORMS');
	var formCount = parseInt(totalFormsInput.val(), 10);
  
	if (opts.onInit) {
		for (var i = 0; i < formCount; i++) {
			opts.onInit(i);
		}
	}
  
	var emptyFormTemplate = document.getElementById(prefix + '-EMPTY_FORM_TEMPLATE');
	if (emptyFormTemplate.innerText) {
		emptyFormTemplate = emptyFormTemplate.innerText;
	} else if (emptyFormTemplate.textContent) {
		emptyFormTemplate = emptyFormTemplate.textContent;
	}
  
	addButton.on('click', function() {
		var pre = prefix.replace(/^id_/, '')  // ADDED WITH RESPECT TO WAGTAIL VERSION
		if (addButton.hasClass('disabled')) return false;
		var newFormHtml = emptyFormTemplate
			.replace(new RegExp(`${pre}-__prefix__`, 'g'), `${pre}-${formCount}`)  // MODIFIED WITH RESPECT TO WAGTAIL VERSION
			.replace(/<-(-*)\/script>/g, '<$1/script>');
		formContainer.append(newFormHtml);
		if (opts.onAdd) opts.onAdd(formCount);
		if (opts.onInit) opts.onInit(formCount);
  
		formCount++;
		totalFormsInput.val(formCount);
	});
  }