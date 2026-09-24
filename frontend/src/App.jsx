import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [url, setUrl] = useState("");
  const [maxPages, setMaxPages] = useState(50);

  const [data, setData] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeWebsite = async () => {
    if (!url.trim()) {
      setError("Please enter a website URL.");
      return;
    }

    setLoading(true);
    setError("");
    setData(null);

    try {
      const response = await fetch(
        `${API_URL}/api/analyze`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            url: url.trim(),
            max_pages: Number(maxPages),
          }),
        }
      );

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.detail || "Analysis failed."
        );
      }

      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };


  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      analyzeWebsite();
    }
  };


  return (
    <div className="app">

      {/* -------------------------------- */}
      {/* SIDEBAR */}
      {/* -------------------------------- */}

      <aside className="sidebar">

        <div className="brand">

          <div className="brand-icon">
            S
          </div>

          <div>
            <h1>SiteScope</h1>

            <p>
              Semantic SEO Analyzer
            </p>
          </div>

        </div>


        <div className="sidebar-section">

          <span className="sidebar-label">
            ANALYSIS
          </span>

          <div className="sidebar-item active">
            <span>◈</span>
            Site Overview
          </div>

          <div className="sidebar-item">
            <span>◎</span>
            Topical Clusters
          </div>

          <div className="sidebar-item">
            <span>↗</span>
            Link Opportunities
          </div>

        </div>


        <div className="sidebar-bottom">

          <div className="project-status">

            <span className="status-dot"></span>

            <div>
              <strong>Analysis Engine</strong>
              <small>Connected to API</small>
            </div>

          </div>

        </div>

      </aside>


      {/* -------------------------------- */}
      {/* MAIN CONTENT */}
      {/* -------------------------------- */}

      <main className="main">

        {/* HEADER */}

        <header className="topbar">

          <div>
            <h2>
              Semantic Site Architecture
            </h2>

            <p>
              Discover topical clusters, internal-link relationships,
              and semantic link opportunities.
            </p>
          </div>

        </header>


        {/* -------------------------------- */}
        {/* WEBSITE INPUT */}
        {/* -------------------------------- */}

        <section className="analyze-panel">

          <div className="input-area">

            <label>
              Website URL
            </label>

            <input
              type="text"
              placeholder="https://example.com"
              value={url}
              onChange={(event) =>
                setUrl(event.target.value)
              }
              onKeyDown={handleKeyDown}
            />

          </div>


          <div className="page-limit">

            <label>
              Max pages
            </label>

            <input
              type="number"
              min="1"
              max="200"
              value={maxPages}
              onChange={(event) =>
                setMaxPages(event.target.value)
              }
            />

          </div>


          <button
            className="analyze-button"
            onClick={analyzeWebsite}
            disabled={loading}
          >

            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing...
              </>
            ) : (
              <>
                Analyze Website
                <span>→</span>
              </>
            )}

          </button>

        </section>


        {/* ERROR */}

        {error && (

          <div className="error-box">
            <strong>Analysis failed</strong>
            <span>{error}</span>
          </div>

        )}


        {/* -------------------------------- */}
        {/* EMPTY STATE */}
        {/* -------------------------------- */}

        {!data && !loading && !error && (

          <section className="empty-state">

            <div className="empty-icon">
              ◇
            </div>

            <h3>
              Analyze a website to get started
            </h3>

            <p>
              Enter a website above and SiteScope will crawl its pages,
              identify semantic relationships, discover topical clusters,
              and find potential internal-link opportunities.
            </p>

          </section>

        )}


        {/* -------------------------------- */}
        {/* RESULTS */}
        {/* -------------------------------- */}

        {data && (

          <>

            {/* SUMMARY CARDS */}

            <section className="stats-grid">

              <StatCard
                label="Pages Crawled"
                value={data.summary.pages}
                icon="▦"
              />

              <StatCard
                label="Internal Links"
                value={data.summary.internal_links}
                icon="↗"
              />

              <StatCard
                label="Topical Clusters"
                value={data.summary.clusters}
                icon="◉"
              />

              <StatCard
                label="Link Opportunities"
                value={
                  data.summary.link_opportunities
                }
                icon="✦"
              />

            </section>


            {/* TWO COLUMN CONTENT */}

            <section className="content-grid">

              {/* PAGES */}

              <div className="panel">

                <div className="panel-header">

                  <div>
                    <h3>
                      Crawled Pages
                    </h3>

                    <p>
                      Pages discovered during the crawl
                    </p>
                  </div>

                  <span className="count-badge">
                    {data.pages.length}
                  </span>

                </div>


                <div className="table-container">

                  <table>

                    <thead>

                      <tr>
                        <th>Page</th>
                        <th>Cluster</th>
                        <th>Content</th>
                      </tr>

                    </thead>


                    <tbody>

                      {data.pages.map(
                        (page, index) => (

                          <tr key={index}>

                            <td>

                              <div className="page-cell">

                                <strong>
                                  {page.title ||
                                    "Untitled page"}
                                </strong>

                                <span>
                                  {page.url}
                                </span>

                              </div>

                            </td>


                            <td>

                              <span className="cluster-badge">
                                Cluster{" "}
                                {page.cluster + 1}
                              </span>

                            </td>


                            <td>
                              {page.content_length.toLocaleString()}{" "}
                              chars
                            </td>

                          </tr>

                        )
                      )}

                    </tbody>

                  </table>

                </div>

              </div>


              {/* CLUSTERS */}

              <div className="panel">

                <div className="panel-header">

                  <div>
                    <h3>
                      Topical Clusters
                    </h3>

                    <p>
                      Semantic grouping of pages
                    </p>
                  </div>

                </div>


                <div className="cluster-list">

                  {data.clusters.map(
                    (cluster) => (

                      <div
                        className="cluster-row"
                        key={cluster.id}
                      >

                        <div className="cluster-number">
                          {cluster.id + 1}
                        </div>

                        <div className="cluster-info">

                          <strong>
                            Cluster {cluster.id + 1}
                          </strong>

                          <span>
                            {cluster.page_count}{" "}
                            {cluster.page_count === 1
                              ? "page"
                              : "pages"}
                          </span>

                        </div>


                        <div className="cluster-bar">

                          <div
                            className="cluster-bar-fill"
                            style={{
                              width: `${Math.max(
                                8,
                                (
                                  cluster.page_count /
                                  Math.max(
                                    ...data.clusters.map(
                                      (c) =>
                                        c.page_count
                                    )
                                  )
                                ) *
                                  100
                              )}%`,
                            }}
                          />

                        </div>

                      </div>

                    )
                  )}

                </div>

              </div>

            </section>


            {/* -------------------------------- */}
            {/* LINK OPPORTUNITIES */}
            {/* -------------------------------- */}

            <section className="panel opportunities-panel">

              <div className="panel-header">

                <div>

                  <h3>
                    Internal-Link Opportunities
                  </h3>

                  <p>
                    Semantically related pages that are
                    not currently connected by an internal link.
                  </p>

                </div>

                <span className="count-badge">
                  {data.opportunities.length}
                </span>

              </div>


              {data.opportunities.length === 0 ? (

                <div className="no-results">
                  No link opportunities found.
                </div>

              ) : (

                <div className="table-container">

                  <table>

                    <thead>

                      <tr>
                        <th>Source Page</th>
                        <th>Target Page</th>
                        <th>Semantic Similarity</th>
                      </tr>

                    </thead>


                    <tbody>

                      {data.opportunities
                        .slice(0, 25)
                        .map(
                          (opportunity, index) => (

                            <tr key={index}>

                              <td>

                                <span className="url-text">
                                  {opportunity.source}
                                </span>

                              </td>

                              <td>

                                <span className="url-text">
                                  {opportunity.target}
                                </span>

                              </td>

                              <td>

                                <div className="similarity">

                                  <div className="similarity-bar">

                                    <div
                                      className="similarity-fill"
                                      style={{
                                        width: `${Math.min(
                                          100,
                                          opportunity.similarity *
                                            100
                                        )}%`,
                                      }}
                                    />

                                  </div>

                                  <strong>
                                    {(
                                      opportunity.similarity *
                                      100
                                    ).toFixed(1)}
                                    %
                                  </strong>

                                </div>

                              </td>

                            </tr>

                          )
                        )}

                    </tbody>

                  </table>

                </div>

              )}

            </section>


            {/* -------------------------------- */}
            {/* GRAPH SUMMARY */}
            {/* -------------------------------- */}

            <section className="graph-panel">

              <div>

                <span className="graph-label">
                  INTERNAL-LINK GRAPH
                </span>

                <h3>
                  Website Architecture
                </h3>

                <p>
                  Your crawl contains{" "}
                  <strong>
                    {data.graph.nodes.length}
                  </strong>{" "}
                  pages connected through{" "}
                  <strong>
                    {data.graph.edges.length}
                  </strong>{" "}
                  internal links.
                </p>

              </div>


              <div className="graph-stat">

                <strong>
                  {data.graph.nodes.length}
                </strong>

                <span>
                  Nodes
                </span>

              </div>


              <div className="graph-stat">

                <strong>
                  {data.graph.edges.length}
                </strong>

                <span>
                  Edges
                </span>

              </div>

            </section>

          </>

        )}

      </main>

    </div>
  );
}


/* -------------------------------- */
/* STAT CARD */
/* -------------------------------- */

function StatCard({
  label,
  value,
  icon,
}) {

  return (

    <div className="stat-card">

      <div className="stat-icon">
        {icon}
      </div>

      <div>

        <span>
          {label}
        </span>

        <strong>
          {value.toLocaleString()}
        </strong>

      </div>

    </div>

  );
}


export default App;