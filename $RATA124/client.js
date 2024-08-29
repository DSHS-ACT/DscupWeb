
if (!localStorage.getItem('deviceId')) {
    localStorage.setItem('deviceId', Date.now().toString(36) + Math.random().toString(36).substr(2));
  }
  
  
  async function vote(playerNumber) {
    const response = await fetch('/vote', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            player_number: playerNumber,
            device_id: localStorage.getItem('deviceId')
        })
    });
    const result = await response.json();
    alert(result.message || result.error);
  }