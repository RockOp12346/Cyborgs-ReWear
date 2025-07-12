class Modal {
    constructor(title, content) {
        this.title = title;
        this.content = content;
    }

    create() {
        const modalHTML = `
            <div class="modal fade" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${this.title}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            ${this.content}
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = modalHTML;
        document.body.appendChild(tempDiv.firstElementChild);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const infoModal = new Modal('Welcome', 'This is a modern web application with interactive features.');
    infoModal.create();
});