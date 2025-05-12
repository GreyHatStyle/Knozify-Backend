// Since django and python isn't able to send the request for some reason I will send it using node js
// and call it using subprocess in python

async function sendSmsWithFetch(apiUrl, apiKey, recipients, message) {
  const payload = {
    recipients: [recipients], 
    message: message
  };

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'x-api-key': apiKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {

      const errorData = await response.json().catch(() => ({ message: response.statusText }));
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.message || 'Unknown error'}`);
    }

    const data = await response.json();
    console.log('SMS sent successfully!');
    console.log('Response:', data);
    return data;

  } catch (error) {
    console.error('Error sending SMS:', error);
    throw error;
  }
}

// Get command line arguments
// process.argv[0] is node executable
// process.argv[1] is the script path
const args = process.argv.slice(2);

if (args.length < 4) {
  console.error("Usage: node api-sendsms.js <apiUrl> <apiKey> <recipientPhoneNumber> <message>");
  process.exit(1); // Exit with an error code
}

const [cliApiUrl, cliApiKey, cliRecipient, cliMessage] = args;

sendSmsWithFetch(cliApiUrl, cliApiKey, cliRecipient, cliMessage)
  .then(result => console.log('Operation completed successfully.'))
  .catch(err => console.error('Operation failed.'));

