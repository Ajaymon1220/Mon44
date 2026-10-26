import { ThemeToggle } from './components/ThemeToggle';

const foundations = [
  { number: '01', title: 'Make it yours.', copy: 'A fresh canvas for your idea. The colors, the words, the details — it all starts here.' },
  { number: '02', title: 'Room to grow.', copy: 'Start with a page. Add your story, your products, or your next big thing as we build.' },
  { number: '03', title: 'Every screen, considered.', copy: 'A comfortable starting point on your phone, your laptop, and everything in between.' },
];

export default function App() {
  return (
    <div className="site-shell">
      <a className="skip-link" href="#main">Skip to content</a>
      <header className="site-header">
        <a className="brand" href="#" aria-label="Canvas home"><span className="brand-icon" aria-hidden="true">c</span>canvas<span className="brand-dot">.</span></a>
        <div className="header-actions"><a className="nav-link" href="#foundation">The foundation</a><ThemeToggle /></div>
      </header>
      <main id="main">
        <section className="hero" aria-labelledby="hero-title">
          <div className="hero-copy">
            <p className="eyebrow"><span className="status-dot" /> A LITTLE SPACE FOR A BIG IDEA</p>
            <h1 id="hero-title">Good things<br />start with a<br /><span>blank canvas.</span></h1>
            <p className="hero-description">This is the beginning. A place to turn a spark of an idea into something you can see, feel, and share.</p>
            <a className="button" href="#foundation">Explore the foundation <span aria-hidden="true">↗</span></a>
            <p className="hero-note">Your idea. Our next chapter.</p>
          </div>
          <div className="art-board" role="img" aria-label="Abstract geometric composition with a green circle, an arch, and a checkerboard">
            <div className="art-topline"><span>IDEAS IN THE MAKING</span><span>001 / ∞</span></div>
            <div className="art-circle" /><div className="art-arch" /><div className="art-checker" />
            <span className="art-star" aria-hidden="true">✳</span>
            <div className="art-label">A work in possibility.<span>↗</span></div>
          </div>
        </section>
        <section className="foundation" id="foundation" aria-labelledby="foundation-title">
          <div className="section-heading"><h2 id="foundation-title">A simple start. Endless possibilities.</h2><span>BUILT FROM HERE ↘</span></div>
          <div className="card-grid">{foundations.map(item => (
            <article className="feature-card" key={item.number}><span className="card-number">{item.number}</span><h3>{item.title}</h3><p>{item.copy}</p></article>
          ))}</div>
        </section>
      </main>
      <footer><span>canvas. <span className="footer-muted">A fresh start.</span></span><span>Made to become something.</span></footer>
    </div>
  );
}
