const el = (id) => document.getElementById(id);

const state = {
  apiBase: "/api/v1",
  projectId: null,
  projectName: "",
  route: "/projects",
  projects: [],
  world: [],
  characters: [],
  outlines: [],
  chapters: [],
  chapterSide: { recent: [], fores: [], review: "" },
  memoryTab: "fores",
  chapterTab: "recent",
};

function showToast(msg, type = "info") {
  const t = el("toast");
  t.textContent = msg;
  t.className = `toast show ${type}`;
  setTimeout(() => (t.className = "toast"), 2200);
}

function setLoading(btn, loading) {
  if (!btn) return;
  if (loading) {
    btn.dataset.old = btn.textContent;
    btn.textContent = "加载中...";
    btn.disabled = true;
  } else {
    btn.textContent = btn.dataset.old || btn.textContent;
    btn.disabled = false;
  }
}

function requireProject() {
  if (!state.projectId) throw new Error("请先选择项目");
  return state.projectId;
}

function updateTopbar() {
  el("current-project-name").textContent = state.projectId ? `${state.projectName} (#${state.projectId})` : "未选择";
  const stageMap = {
    "/projects": "项目列表",
    overview: "项目概览",
    proposal: "Proposal",
    world: "世界观",
    characters: "角色",
    outlines: "大纲",
    chapters: "章节",
    memory: "记忆中心",
    review: "审校中心",
    settings: "设置",
  };
  const key = state.route.includes("/projects/") ? state.route.split("/").pop() : "/projects";
  el("current-stage").textContent = stageMap[key] || "项目列表";
}

function api(path) {
  const base = (el("api-prefix").value || state.apiBase).trim().replace(/\/$/, "");
  return `${base}${path}`;
}

async function request(method, path, body, loadingBtn) {
  setLoading(loadingBtn, true);
  try {
    const resp = await fetch(api(path), {
      method,
      headers: { "Content-Type": "application/json" },
      body: body ? JSON.stringify(body) : undefined,
    });
    const text = await resp.text();
    let data;
    try { data = text ? JSON.parse(text) : {}; } catch { data = text; }
    if (!resp.ok) {
      const msg = data?.detail || data?.message || `请求失败 ${resp.status}`;
      showToast(msg, "error");
      throw new Error(msg);
    }
    return data;
  } catch (e) {
    showToast(e.message || "请求异常", "error");
    throw e;
  } finally {
    setLoading(loadingBtn, false);
  }
}

function hideAllPages() {
  document.querySelectorAll(".page").forEach((p) => p.classList.remove("active"));
  document.querySelectorAll(".side-item").forEach((b) => b.classList.remove("active"));
}

function toPath(route) {
  if (route.includes(":id")) {
    if (!state.projectId) return "/projects";
    return route.replace(":id", String(state.projectId));
  }
  return route;
}

function navigate(route, options = {}) {
  const target = toPath(route);
  if (target === "/projects") state.route = "/projects";
  else state.route = target;

  hideAllPages();

  if (state.route === "/projects") el("page-projects").classList.add("active");
  else if (state.route.endsWith("/overview")) el("page-overview").classList.add("active");
  else if (state.route.endsWith("/proposal")) el("page-proposal").classList.add("active");
  else if (state.route.endsWith("/world")) el("page-world").classList.add("active");
  else if (state.route.endsWith("/characters")) el("page-characters").classList.add("active");
  else if (state.route.endsWith("/outlines")) el("page-outlines").classList.add("active");
  else if (state.route.endsWith("/chapters")) el("page-chapters").classList.add("active");
  else if (state.route.endsWith("/memory")) el("page-memory").classList.add("active");
  else if (state.route.endsWith("/review")) el("page-review").classList.add("active");
  else if (state.route.endsWith("/settings")) el("page-settings").classList.add("active");

  document.querySelectorAll(".side-item").forEach((btn) => {
    const r = toPath(btn.dataset.route);
    if (r === state.route) btn.classList.add("active");
  });

  updateTopbar();
  if (!options.silent) loadRouteData();
}

function card(title, body) {
  return `<div class="card-mini"><h4>${title}</h4><p>${body}</p></div>`;
}

function renderProjects(list) {
  const kw = (el("project-keyword").value || "").trim().toLowerCase();
  const filtered = !kw ? list : list.filter((p) => String(p.id).includes(kw) || String(p.title || "").toLowerCase().includes(kw));
  if (!filtered.length) {
    el("project-list").innerHTML = '<div class="panel">暂无匹配项目</div>';
    return;
  }
  el("project-list").innerHTML = filtered.map((p) => `
    <div class="list-item">
      <div><strong>${p.title || "(无标题)"}</strong> <span>#${p.id}</span><div class="muted">${p.genre || "-"} · ${p.platform_style || "-"} · ${p.tone || "-"}</div><div class="muted">${p.summary || ""}</div></div>
      <button class="ghost" data-enter="${p.id}" data-name="${(p.title || "").replace(/"/g, "&quot;")}">进入项目</button>
    </div>
  `).join("");
  el("project-list").querySelectorAll("[data-enter]").forEach((b) => {
    b.onclick = () => {
      state.projectId = Number(b.dataset.enter);
      state.projectName = b.dataset.name || "";
      navigate("/projects/:id/overview");
    };
  });
}

async function refreshProjects(btn) {
  state.projects = await request("GET", "/projects", null, btn);
  renderProjects(state.projects);
}

async function loadOverview() {
  const pid = requireProject();
  const [p, w, c, o, ch, f, t] = await Promise.all([
    request("GET", `/projects/${pid}`),
    request("GET", `/projects/${pid}/world`),
    request("GET", `/projects/${pid}/characters`),
    request("GET", `/projects/${pid}/outlines`),
    request("GET", `/projects/${pid}/chapters`),
    request("GET", `/projects/${pid}/memory/foreshadowings`),
    request("GET", `/projects/${pid}/memory/timeline`),
  ]);

  el("overview-info").innerHTML = [
    card("项目名称", p.title || "-"), card("题材", p.genre || "-"), card("平台风格", p.platform_style || "-"),
    card("基调", p.tone || "-"), card("简介", p.summary || "-"),
  ].join("");

  const progress = [
    ["项目创建", !!p.id], ["世界观生成", (w.world || []).length > 0], ["角色生成", (c.characters || []).length > 0],
    ["大纲生成", (o.outlines || []).length > 0], ["章节生成", (ch.chapters || []).length > 0],
  ];
  el("overview-progress").innerHTML = progress.map(([k, ok]) => card(k, ok ? "已完成" : "未完成")).join("");

  el("overview-stats").innerHTML = [
    card("角色数", String((c.characters || []).length)),
    card("章节数", String((ch.chapters || []).length)),
    card("开放伏笔", String((f.foreshadowings || []).length)),
    card("时间线事件", String((t.timeline || []).length)),
  ].join("");
}

async function loadWorld() {
  const pid = requireProject();
  const res = await request("GET", `/projects/${pid}/world`);
  const world = res.world || [];
  if (!world.length) {
    el("world-panel").innerHTML = '<div class="panel">暂无世界观数据，点击“生成世界观”</div>';
    return;
  }
  el("world-panel").innerHTML = world.map((x) => card(x.key_name || "world", x.content_json || "")).join("");
}

async function loadCharacters() {
  const pid = requireProject();
  const res = await request("GET", `/projects/${pid}/characters`);
  state.characters = res.characters || [];
  if (!state.characters.length && res.raw) {
    el("character-list").innerHTML = '<div class="panel">角色结构化解析失败，已返回 raw</div>';
    el("character-detail").textContent = JSON.stringify(res.raw, null, 2);
    return;
  }
  el("character-list").innerHTML = state.characters.map((c, i) => `<div class="list-item"><button class="ghost" data-char="${i}">${c.name || "-"} (${c.role || "-"})</button></div>`).join("");
  el("character-list").querySelectorAll("[data-char]").forEach((b) => {
    b.onclick = () => {
      const c = state.characters[Number(b.dataset.char)] || {};
      el("character-detail").textContent = JSON.stringify(c, null, 2);
    };
  });
  el("character-detail").textContent = state.characters[0] ? JSON.stringify(state.characters[0], null, 2) : "请选择角色查看详情";
}

async function loadOutlines() {
  const pid = requireProject();
  const res = await request("GET", `/projects/${pid}/outlines`);
  state.outlines = res.outlines || [];
  if (!state.outlines.length) {
    el("outline-tree").innerHTML = '<div class="panel">暂无大纲</div>';
    el("outline-detail").textContent = "请选择大纲查看详情";
    return;
  }
  el("outline-tree").innerHTML = state.outlines.map((o, i) => `<div class="list-item"><button class="ghost" data-outline="${i}">[${o.level}] ${o.title || "-"} (#${o.ref_no})</button></div>`).join("");
  el("outline-tree").querySelectorAll("[data-outline]").forEach((b) => {
    b.onclick = () => {
      const o = state.outlines[Number(b.dataset.outline)] || {};
      el("outline-detail").textContent = JSON.stringify(o, null, 2);
      if (o.level === "chapter") {
        const no = Number(o.ref_no || 1);
        el("chapter-no").value = String(no);
      }
    };
  });
  el("outline-detail").textContent = JSON.stringify(state.outlines[0], null, 2);
}

async function loadChapters() {
  const pid = requireProject();
  const res = await request("GET", `/projects/${pid}/chapters`);
  state.chapters = res.chapters || [];
  if (!state.chapters.length) {
    el("chapter-list").innerHTML = '<div class="panel">暂无章节</div>';
    return;
  }
  el("chapter-list").innerHTML = state.chapters.map((c) => `<div class="list-item"><button class="ghost" data-ch="${c.chapter_no}">第${c.chapter_no}章 ${c.title || "-"} [${c.status || "draft"}]</button></div>`).join("");
  el("chapter-list").querySelectorAll("[data-ch]").forEach((b) => {
    b.onclick = () => {
      el("chapter-no").value = b.dataset.ch;
      loadSingleChapter();
    };
  });
}

async function loadSingleChapter() {
  const pid = requireProject();
  const no = Number(el("chapter-no").value);
  const c = await request("GET", `/projects/${pid}/chapters/${no}`);
  el("chapter-title").value = c.title || "";
  el("chapter-content").value = c.content || "";
  el("chapter-summary").value = c.summary || "";
  el("chapter-status").value = c.status || "draft";
}

async function loadMemoryTab() {
  const pid = requireProject();
  const tab = state.memoryTab;
  el("memory-search-form").classList.toggle("hidden", tab !== "search");
  if (tab === "fores") {
    const r = await request("GET", `/projects/${pid}/memory/foreshadowings`);
    el("memory-content").textContent = JSON.stringify(r.foreshadowings || [], null, 2);
  } else if (tab === "timeline") {
    const r = await request("GET", `/projects/${pid}/memory/timeline`);
    el("memory-content").textContent = JSON.stringify(r.timeline || [], null, 2);
  } else if (tab === "recent") {
    const r = await request("GET", `/projects/${pid}/memory/recent`);
    el("memory-content").textContent = JSON.stringify(r.memory || [], null, 2);
  } else {
    el("memory-content").textContent = "请输入 query 并点击检索";
  }
}

async function loadRouteData() {
  if (state.route === "/projects") return refreshProjects();
  if (state.route.endsWith("/overview")) return loadOverview();
  if (state.route.endsWith("/world")) return loadWorld();
  if (state.route.endsWith("/characters")) return loadCharacters();
  if (state.route.endsWith("/outlines")) return loadOutlines();
  if (state.route.endsWith("/chapters")) return loadChapters();
  if (state.route.endsWith("/memory")) return loadMemoryTab();
}

function bindSideNav() {
  document.querySelectorAll(".side-item").forEach((btn) => {
    btn.onclick = () => {
      const route = btn.dataset.route;
      if (route.includes(":id") && !state.projectId) {
        showToast("请先在项目列表选择项目", "error");
        navigate("/projects", { silent: true });
        return;
      }
      navigate(route);
    };
  });
}

function bindOverviewQuickActions() {
  document.querySelectorAll(".quick-actions [data-go]").forEach((b) => {
    b.onclick = () => navigate(`/projects/:id/${b.dataset.go}`);
  });
}

function bindTabs() {
  document.querySelectorAll("[data-memory-tab]").forEach((b) => {
    b.onclick = () => {
      document.querySelectorAll("[data-memory-tab]").forEach((x) => x.classList.remove("active"));
      b.classList.add("active");
      state.memoryTab = b.dataset.memoryTab;
      loadMemoryTab();
    };
  });

  document.querySelectorAll("[data-ch-tab]").forEach((b) => {
    b.onclick = () => {
      document.querySelectorAll("[data-ch-tab]").forEach((x) => x.classList.remove("active"));
      b.classList.add("active");
      state.chapterTab = b.dataset.chTab;
      if (state.chapterTab === "recent") el("chapter-side").textContent = JSON.stringify(state.chapterSide.recent || [], null, 2);
      if (state.chapterTab === "fores") el("chapter-side").textContent = JSON.stringify(state.chapterSide.fores || [], null, 2);
      if (state.chapterTab === "review") el("chapter-side").textContent = String(state.chapterSide.review || "");
    };
  });
}

function bindActions() {
  el("btn-back-projects").onclick = () => navigate("/projects");

  el("project-keyword").addEventListener("input", () => renderProjects(state.projects));
  el("btn-refresh-projects").onclick = () => refreshProjects(el("btn-refresh-projects"));
  el("btn-open-create").onclick = () => el("create-project-box").classList.toggle("hidden");

  el("btn-create-project").onclick = async () => {
    const title = el("cp-title").value.trim();
    const genre = el("cp-genre").value;
    const style = document.querySelector('input[name="cp-style"]:checked')?.value;
    if (!title || !genre || !style) return showToast("请填写必填项", "error");
    const btn = el("btn-create-project");
    const data = await request("POST", "/projects", {
      title,
      genre,
      platform_style: style,
      tone: el("cp-tone").value,
      audience: el("cp-audience").value,
      summary: el("cp-summary").value,
    }, btn);
    showToast("创建成功", "ok");
    state.projectId = data.id;
    state.projectName = data.title || "";
    await refreshProjects();
    navigate("/projects/:id/overview");
  };

  el("btn-generate-proposal").onclick = async () => {
    const idea = el("proposal-idea").value.trim();
    if (!idea) return showToast("请输入创意", "error");
    const r = await request("POST", "/agent/proposal", { user_idea: idea }, el("btn-generate-proposal"));
    el("proposal-result").textContent = typeof r.proposal === "string" ? r.proposal : JSON.stringify(r, null, 2);
  };

  el("btn-copy-proposal").onclick = async () => {
    const txt = el("proposal-result").textContent || "";
    if (!txt.trim()) return showToast("暂无可复制内容", "error");
    await navigator.clipboard.writeText(txt);
    showToast("已复制", "ok");
  };

  el("btn-generate-world").onclick = async () => {
    const pid = requireProject();
    await request("POST", `/projects/${pid}/world/generate`, {}, el("btn-generate-world"));
    await loadWorld();
  };
  el("btn-get-world").onclick = () => loadWorld();

  el("btn-generate-characters").onclick = async () => {
    const pid = requireProject();
    const count = Number(el("character-count").value);
    if (!count) return showToast("角色数量必填", "error");
    const r = await request("POST", `/projects/${pid}/characters/generate`, { character_count: count }, el("btn-generate-characters"));
    if ((!r.characters || !r.characters.length) && r.raw) showToast("结构化解析可能失败，已展示 raw", "error");
    await loadCharacters();
  };
  el("btn-get-characters").onclick = () => loadCharacters();

  el("btn-generate-outlines").onclick = async () => {
    const pid = requireProject();
    const volume_no = Number(el("outline-volume").value);
    const chapter_count = Number(el("outline-ch-count").value);
    if (!volume_no || !chapter_count) return showToast("卷号和章节数必填", "error");
    const r = await request("POST", `/projects/${pid}/outlines/generate`, { volume_no, chapter_count }, el("btn-generate-outlines"));
    if (r.outline?.raw_text) showToast("收到 raw_text，已展示", "error");
    await loadOutlines();
  };
  el("btn-get-outlines").onclick = () => loadOutlines();

  el("btn-generate-chapter").onclick = async () => {
    const pid = requireProject();
    const no = Number(el("chapter-no").value);
    const word_count = Number(el("chapter-word-count").value);
    if (!no || !word_count) return showToast("章节号和字数必填", "error");
    await request("POST", `/projects/${pid}/chapters/${no}/generate`, { word_count, extra_requirements: el("chapter-extra").value }, el("btn-generate-chapter"));
    await loadChapters();
    await loadSingleChapter();
    const [recent, fores] = await Promise.all([
      request("GET", `/projects/${pid}/memory/recent`),
      request("GET", `/projects/${pid}/memory/foreshadowings`),
    ]);
    state.chapterSide.recent = recent.memory || [];
    state.chapterSide.fores = fores.foreshadowings || [];
    document.querySelector('[data-ch-tab="recent"]').click();
  };

  el("btn-load-chapter").onclick = () => loadSingleChapter();

  el("btn-save-chapter").onclick = async () => {
    const pid = requireProject();
    const no = Number(el("chapter-no").value);
    if (!no) return showToast("请选择章节", "error");
    await request("PUT", `/projects/${pid}/chapters/${no}`, {
      title: el("chapter-title").value,
      content: el("chapter-content").value,
      summary: el("chapter-summary").value,
      status: el("chapter-status").value,
    }, el("btn-save-chapter"));
    showToast("保存成功", "ok");
    await loadChapters();
  };

  el("btn-review-chapter").onclick = async () => {
    const pid = requireProject();
    const no = Number(el("chapter-no").value);
    if (!no) return showToast("请选择章节", "error");
    const r = await request("POST", `/projects/${pid}/chapters/${no}/review`, {}, el("btn-review-chapter"));
    state.chapterSide.review = r.review || JSON.stringify(r, null, 2);
    document.querySelector('[data-ch-tab="review"]').click();
  };

  el("btn-memory-search").onclick = async () => {
    const pid = requireProject();
    const query = el("memory-query").value.trim();
    const top_k = Number(el("memory-topk").value);
    if (!query) return showToast("query 必填", "error");
    const r = await request("GET", `/projects/${pid}/memory/search?query=${encodeURIComponent(query)}&top_k=${top_k}`, null, el("btn-memory-search"));
    el("memory-content").textContent = JSON.stringify(r.results || r, null, 2);
  };

  el("btn-run-review").onclick = async () => {
    const pid = requireProject();
    const no = Number(el("review-chapter-no").value);
    if (!no) return showToast("章节号必填", "error");
    const r = await request("POST", `/projects/${pid}/chapters/${no}/review`, {}, el("btn-run-review"));
    el("review-result").textContent = typeof r.review === "string" ? r.review : JSON.stringify(r, null, 2);
  };
}

function init() {
  bindSideNav();
  bindOverviewQuickActions();
  bindTabs();
  bindActions();
  navigate("/projects", { silent: true });
  refreshProjects();
}

window.addEventListener("DOMContentLoaded", init);
