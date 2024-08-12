function confirmDelete(id) {
    if (confirm("Are you sure you want to delete this user?")) {
        fetch(`/delete/${id}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to delete user');
            }
            return response.json();
        })
        .then(data => {
            console.log('User deleted:', data);
            location.reload();  // Reload the page to reflect changes
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}
