document.addEventListener('DOMContentLoaded', () => {
	const form = document.getElementById('form');
	const userInput = document.getElementById('url');
	const error = document.getElementById('error');
	const summaryBlock = document.getElementById('summary-block');
	const spinner = document.getElementById('spinner');
	const summary = document.getElementById('summary');
	const copyButton = document.getElementById('copy-button');

	// On submit behavior for the URL input field
	form.addEventListener('submit', (event) => {

		// Prevent the page from refreshing upon user submission
		event.preventDefault();

		// Validate user input
		const url = userInput.value.trim();
		if (isValidUrl(url)) {
			if (url.includes('arxiv')) {
				error.classList.add('hidden');
			}
			else {
				error.textContent = 'Please enter a link to a paper from arxiv.org';
				error.classList.remove('hidden');
				return;
			}
		}
		else {
			error.textContent = 'Please enter a valid URL';
			error.classList.remove('hidden');
			return;
		}

		// Show all elements of the summary block (i.e., the label for the summary card, the summary card and the spinner), except the summary text
		summaryBlock.classList.remove('hidden');
		spinner.classList.remove('hidden');
		summary.classList.add('hidden');

		// Call the summarize API
		fetch('/summarize', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ url: url })
		})
		.then(response => response.json())
		.then(data => {
			// Upon successful return from summarize API, hide the spinner and show the summary text
			spinner.classList.add('hidden');
			summary.classList.remove('hidden');
			summary.textContent = data.summary;
		})
		.catch(error => {
			// In case of errors, display the error in console and as the summary text
			console.error('Error: ', url);
			spinner.classList.add('hidden');
			summary.classList.remove('hidden');
			summary.textContent = error;
		});
  	});

	// On click behavior for the copy button at the top right of the summary card
	copyButton.addEventListener('click', () => {
		navigator.clipboard.writeText(summary.innerText);
	});
});

// Helper function to determine if a string is a valid URL
function isValidUrl(string) {
	try {
		new URL(string);
		return true;
	}
	catch (error) {
		return false;
	}
}