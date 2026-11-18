import React from 'react';
import { ShoppingBag, ExternalLink, ShieldCheck, Ruler, Palette, Shapes } from 'lucide-react';

export default function ProductList({
  products = [],
  totalCost = 0,
  hoveredProductId,
  setHoveredProductId
}) {
  if (!products.length) return null;

  return (
    <div className="product-list-card">
      <div className="list-header">
        <div>
          <h3 className="list-title">Purchasable Products in this Design</h3>
          <p className="list-subtitle">Real verified products dimension-checked to fit your room floor plan.</p>
        </div>

        <div className="total-budget-badge">
          <span className="total-label">Total Room Setup:</span>
          <strong className="total-val">₹{totalCost?.toLocaleString('en-IN') || '0'}</strong>
        </div>
      </div>

      <div className="products-grid">
        {products.map((prod, idx) => {
          const isHovered = hoveredProductId === prod.id;
          const dim = prod.dimensions || {};
          const storeLower = (prod.store || 'amazon').toLowerCase().replace('.', '');

          return (
            <div
              key={prod.id || idx}
              id={`card-${prod.id}`}
              className={`product-card ${isHovered ? 'hovered' : ''}`}
              onMouseEnter={() => setHoveredProductId(prod.id)}
              onMouseLeave={() => setHoveredProductId(null)}
            >
              {/* Product Thumbnail with Badges */}
              <div className="card-thumb-wrap">
                <img
                  src={prod.cutout_url || prod.image_url}
                  alt={prod.title}
                  className="card-thumb"
                  loading="lazy"
                />
                <span className={`store-badge store-${storeLower}`}>{prod.store}</span>
                <span className="card-pin-idx">{idx + 1}</span>
              </div>

              {/* Product Info & Specs */}
              <div className="card-body">
                <span className="card-category">{(prod.category || 'furniture').replace('_', ' ').toUpperCase()}</span>
                <h4 className="card-title" title={prod.title}>{prod.title}</h4>

                {/* Dimension Tag */}
                <div className="dimension-badge">
                  <Ruler size={13} className="text-cyan-400" />
                  <span>
                    Fit: {dim.width_in || 40}"W × {dim.depth_in || 28}"D × {dim.height_in || 30}"H
                  </span>
                </div>

                {/* Shape & Color Attributes */}
                <div className="card-attributes">
                  {prod.shape && (
                    <span className="attr-pill shape-pill" title="Geometric Shape">
                      <Shapes size={11} />
                      {prod.shape}
                    </span>
                  )}
                  {prod.color && (
                    <span className="attr-pill color-pill" title="Color Palette">
                      <span className="color-dot"></span>
                      {prod.color}
                    </span>
                  )}
                </div>

                {/* Price & Buy Button */}
                <div className="card-footer">
                  <div className="price-wrap">
                    <span className="price-tag">₹{(prod.price_inr || 0).toLocaleString('en-IN')}</span>
                  </div>

                  <a
                    href={prod.buy_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="buy-btn"
                  >
                    <span>Buy on {prod.store}</span>
                    <ExternalLink size={13} />
                  </a>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

