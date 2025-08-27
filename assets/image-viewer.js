// Bildvisar-overlay för artiklar
class ImageViewer {
  constructor() {
    this.currentIndex = 0;
    this.images = [];
    this.overlay = null;
    this.overlayImage = null;
    this.overlayCaption = null;
    this.thumbnails = [];
    
    this.init();
  }

  init() {
    // Lägg till klasser på alla bilder för styling
    this.addImageClasses();
    
    // Skapa overlay HTML
    this.createOverlay();
    
    // Lägg till event listeners för alla bilder
    this.setupImageListeners();
    
    // Lägg till keyboard navigation
    this.setupKeyboardNavigation();
  }

  addImageClasses() {
    // Hitta alla bilder i artiklar och lägg till klasser
    const articleImages = document.querySelectorAll('main article img');
    
    articleImages.forEach((img) => {
      // Lägg till klasser för styling
      img.classList.add('article-image');
      
      // Lägg till klasser på parent p-tag om den finns
      const parentP = img.closest('p');
      if (parentP) {
        parentP.classList.add('image-container');
      }
    });
  }

  createOverlay() {
    // Skapa overlay container
    this.overlay = document.createElement('div');
    this.overlay.className = 'image-overlay';
    this.overlay.innerHTML = `
      <div class="overlay-content">
        <img class="overlay-image" src="" alt="" />
        <div class="overlay-caption"></div>
        
        <button class="overlay-nav prev" aria-label="Föregående bild">‹</button>
        <button class="overlay-nav next" aria-label="Nästa bild">›</button>
        <button class="overlay-close" aria-label="Stäng">×</button>
        
        <div class="overlay-thumbnails"></div>
      </div>
    `;

    // Lägg till i body
    document.body.appendChild(this.overlay);

    // Hitta element
    this.overlayImage = this.overlay.querySelector('.overlay-image');
    this.overlayCaption = this.overlay.querySelector('.overlay-caption');
    this.thumbnailsContainer = this.overlay.querySelector('.overlay-thumbnails');

    // Event listeners för knappar
    this.overlay.querySelector('.overlay-nav.prev').addEventListener('click', () => this.prevImage());
    this.overlay.querySelector('.overlay-nav.next').addEventListener('click', () => this.nextImage());
    this.overlay.querySelector('.overlay-close').addEventListener('click', () => this.closeOverlay());
    
    // Klicka utanför bilden för att stänga
    this.overlay.addEventListener('click', (e) => {
      if (e.target === this.overlay) {
        this.closeOverlay();
      }
    });
  }

  setupImageListeners() {
    // Hitta alla bilder i artikeln (både i figure och direkt)
    const articleImages = document.querySelectorAll('main article img');
    
    articleImages.forEach((img, index) => {
      img.addEventListener('click', () => {
        this.openOverlay(index);
      });
    });
  }

  setupKeyboardNavigation() {
    document.addEventListener('keydown', (e) => {
      if (!this.overlay.classList.contains('active')) return;

      switch (e.key) {
        case 'Escape':
          this.closeOverlay();
          break;
        case 'ArrowLeft':
          this.prevImage();
          break;
        case 'ArrowRight':
          this.nextImage();
          break;
      }
    });
  }

  openOverlay(index) {
    // Samla alla bilder från artikeln
    this.images = Array.from(document.querySelectorAll('main article figure img'));
    this.currentIndex = index;
    
    if (this.images.length === 0) return;

    // Visa bilden
    this.showImage(index);
    
    // Skapa tumnaglar
    this.createThumbnails();
    
    // Visa overlay
    this.overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  showImage(index) {
    const img = this.images[index];
    this.overlayImage.src = img.src;
    this.overlayImage.alt = img.alt;
    
    // Hitta bildtext - kolla både figure/figcaption och efterföljande em-tag
    let caption = '';
    const figure = img.closest('figure');
    if (figure) {
      const figcaption = figure.querySelector('figcaption');
      if (figcaption) {
        caption = figcaption.textContent;
      }
    } else {
      // Om ingen figure, kolla efter efterföljande em-tag (kursiv text)
      const nextElement = img.nextElementSibling;
      if (nextElement && nextElement.tagName === 'EM') {
        caption = nextElement.textContent;
      }
    }
    
    this.overlayCaption.textContent = caption;
    
    // Uppdatera tumnaglar
    this.updateThumbnails();
    
    // Visa/dölj navigeringsknappar
    this.overlay.querySelector('.overlay-nav.prev').style.display = index > 0 ? 'block' : 'none';
    this.overlay.querySelector('.overlay-nav.next').style.display = index < this.images.length - 1 ? 'block' : 'none';
  }

  createThumbnails() {
    this.thumbnailsContainer.innerHTML = '';
    this.thumbnails = [];
    
    this.images.forEach((img, index) => {
      const thumbnail = document.createElement('img');
      thumbnail.className = 'thumbnail';
      thumbnail.src = img.src;
      thumbnail.alt = img.alt;
      thumbnail.addEventListener('click', () => this.showImage(index));
      
      this.thumbnailsContainer.appendChild(thumbnail);
      this.thumbnails.push(thumbnail);
    });
  }

  updateThumbnails() {
    this.thumbnails.forEach((thumb, index) => {
      thumb.classList.toggle('active', index === this.currentIndex);
    });
  }

  prevImage() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      this.showImage(this.currentIndex);
    }
  }

  nextImage() {
    if (this.currentIndex < this.images.length - 1) {
      this.currentIndex++;
      this.showImage(this.currentIndex);
    }
  }

  closeOverlay() {
    this.overlay.classList.remove('active');
    document.body.style.overflow = '';
  }
}

// Initiera bildvisaren när sidan är laddad
document.addEventListener('DOMContentLoaded', () => {
  new ImageViewer();
}); 