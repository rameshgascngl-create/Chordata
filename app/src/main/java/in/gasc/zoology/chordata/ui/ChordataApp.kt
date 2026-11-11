package `in`.gasc.zoology.chordata.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.background
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.List
import androidx.compose.material.icons.filled.School
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.snapshots.SnapshotStateList
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.saveable.listSaver
import androidx.compose.runtime.toMutableStateList
import androidx.activity.compose.BackHandler
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import `in`.gasc.zoology.chordata.data.ProgressStore
import `in`.gasc.zoology.chordata.domain.*

private val teal = Color(0xFF116A67)
private val pale = Color(0xFFF1F7F6)
private val ink = Color(0xFF183238)
private val mutetext = Color(0xFF4D6266)
private val accent = Color(0xFFB25721)
private val paper = Color(0xFFFFFBF5)
private val softGreen = Color(0xFFE9F5F1)
private val softAmber = Color(0xFFFFF1DF)
private val unitColours = listOf(
    Color(0xFFEAF4F0), Color(0xFFFFF1E3), Color(0xFFEDF1FA),
    Color(0xFFF4EFF8), Color(0xFFF1F4E7)
)
private val scheme = lightColorScheme(primary = teal, secondary = accent,
    background = paper, surface = paper, onSurface = ink)

private fun loc(lang: ReadingLanguage, en: String, ta: String): String = if (lang == ReadingLanguage.TA) ta else en

private data class BottomDestination(val tab: String, val label: String, val tamil: String)
private val destinations = listOf(
    BottomDestination("home", "Home", "முகப்பு"),
    BottomDestination("topics", "Lessons", "பாடங்கள்"),
    BottomDestination("practice", "Practice", "பயிற்சி"),
    BottomDestination("saved", "Saved", "சேமிப்பு")
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChordataApp(pack: ContentPack, progress: ProgressStore) {
    var tab by rememberSaveable { mutableStateOf("home") }
    var selectedTopicId by rememberSaveable { mutableStateOf("") }
    var page by rememberSaveable { mutableIntStateOf(0) }
    var languageName by rememberSaveable { mutableStateOf(progress.language().name) }
    val lang = ReadingLanguage.entries.firstOrNull { it.name == languageName } ?: ReadingLanguage.EN
    var textScale by rememberSaveable { mutableFloatStateOf(progress.textScale()) }
    var query by rememberSaveable { mutableStateOf("") }
    var bookmarks by remember { mutableStateOf(progress.bookmarks()) }
    var completed by remember { mutableStateOf(progress.completed()) }
    val currentTopic = pack.findTopic(selectedTopicId)

    fun openTopic(id: String, startPage: Int = 0) {
        selectedTopicId = id
        page = startPage.coerceAtLeast(0)
        tab = "topics"
    }
    fun updateBookmarks(id: String) {
        bookmarks = if (id in bookmarks) bookmarks - id else bookmarks + id
        progress.saveBookmarks(bookmarks)
    }
    fun finishTopic(id: String) {
        completed = completed + id
        progress.saveCompleted(completed)
    }

    BackHandler(enabled = currentTopic != null || tab != "home") {
        if (currentTopic != null) selectedTopicId = "" else tab = "home"
    }
    MaterialTheme(colorScheme = scheme) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = {
                        Column {
                            Text(if (currentTopic != null) loc(lang, "Lesson", "பாடம்")
                                 else loc(lang, "CHORDATA", "முதுகுநாணிகள்"),
                                maxLines = 1, overflow = TextOverflow.Ellipsis,
                                style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                            Text(if (currentTopic == null) (if (lang == ReadingLanguage.TA) "இளநிலை விலங்கியல் · இணையமின்றி" else "B.Sc. Zoology · Offline") else (if (lang == ReadingLanguage.TA) currentTopic.title.ta else currentTopic.title.en),
                                maxLines = 1, overflow = TextOverflow.Ellipsis,
                                style = MaterialTheme.typography.labelSmall, color = mutetext)
                        }
                    },
                    navigationIcon = {
                        if (currentTopic != null) IconButton(
                            onClick = { selectedTopicId = "" },
                            modifier = Modifier.size(48.dp).testTag("lesson-back")
                        ) {
                            Icon(Icons.Default.ArrowBack,
                                contentDescription = loc(lang, "Back to lessons", "பாடங்களுக்குத் திரும்புக"))
                        }
                    },
                    actions = {
                        if (currentTopic != null) {
                            IconButton(onClick = { updateBookmarks(currentTopic.id) },
                                modifier = Modifier.size(48.dp)) {
                                Icon(Icons.Default.Bookmark, contentDescription = if (currentTopic.id in bookmarks)
                                    loc(lang, "Remove bookmark", "சேமிப்பிலிருந்து நீக்கு") else loc(lang, "Save bookmark", "பாடத்தைச் சேமி"),
                                    tint = if (currentTopic.id in bookmarks) accent else mutetext)
                            }
                        }
                    },
                    colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.White)
                )
            },
            bottomBar = {
                // Lesson navigation is handled by the top Back action and the
                // in-chapter pager. Reclaim the navigation bar's vertical space
                // for diagrams and large Tamil text while a lesson is open.
                if (currentTopic == null) {
                    NavigationBar(
                        containerColor = Color.White,
                        modifier = Modifier.testTag("app-bottom-navigation")
                    ) {
                    destinations.forEachIndexed { index, destination ->
                        val ic = when (index) {
                            0 -> Icons.Default.Home
                            1 -> Icons.Default.List
                            2 -> Icons.Default.School
                            else -> Icons.Default.Star
                        }
                        NavigationBarItem(
                            selected = tab == destination.tab,
                            onClick = { selectedTopicId = ""; tab = destination.tab },
                            icon = { Icon(ic, contentDescription = null) },
                            label = { Text(if (lang == ReadingLanguage.TA) destination.tamil else destination.label,
                                maxLines = 1, fontSize = 10.sp) },
                            alwaysShowLabel = true
                        )
                    }
                    }
                }
            }
        ) { insets ->
            Box(Modifier.padding(insets).fillMaxSize()) {
                when {
                    currentTopic != null -> TopicReader(currentTopic, pack, lang, textScale,
                        page, { page = it.coerceIn(0, LearningLogic.lastPage(currentTopic)) },
                        onNextTopic = { LearningLogic.nextTopic(pack, currentTopic.id)?.let { openTopic(it.id) } },
                        onComplete = { finishTopic(currentTopic.id) },
                        completed = currentTopic.id in completed,
                        store = progress)
                    tab == "home" -> HomePage(pack, lang, textScale, completed, bookmarks,
                        onLanguage = { languageName = it.name; progress.saveLanguage(it) },
                        onScale = { textScale = it; progress.saveTextScale(it) },
                        onOpen = { openTopic(it) },
                        onBrowse = { tab = "topics" })
                    else -> ListingPage(pack, tab, query, onQuery = { query = it }, lang, textScale,
                        bookmarks, completed, onOpen = { id ->
                            val topic = pack.findTopic(id)
                            openTopic(id, if (tab == "practice" && topic != null) LearningLogic.lastPage(topic) else 0)
                        })
                }
            }
        }
    }
}

@Composable
private fun BilingualText(value: Bilingual, lang: ReadingLanguage, scale: Float,
    modifier: Modifier = Modifier, base: Float = 16f, bold: Boolean = false,
    alignment: TextAlign = TextAlign.Start) {
    Text(
        if (lang == ReadingLanguage.TA) value.ta else value.en,
        modifier = modifier,
        fontSize = (base * scale).sp,
        lineHeight = (base * scale * if (lang == ReadingLanguage.TA) 1.52f else 1.46f).sp,
        fontWeight = if (bold) FontWeight.SemiBold else FontWeight.Normal,
        textAlign = alignment
    )
}

@Composable
private fun HomePage(pack: ContentPack, lang: ReadingLanguage, scale: Float,
    completed: Set<String>, bookmarks: Set<String>, onLanguage: (ReadingLanguage) -> Unit,
    onScale: (Float) -> Unit, onOpen: (String) -> Unit, onBrowse: () -> Unit) {
    val total = pack.topics.size
    val finished = pack.topics.count { it.id in completed }
    val remaining = pack.topics.firstOrNull { it.id !in completed }
    LazyColumn(
        modifier = Modifier.fillMaxSize().background(paper).testTag("home-book-layout"),
        contentPadding = PaddingValues(horizontal = 14.dp, vertical = 12.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        item(key = "subject-hero") {
            Card(
                shape = RoundedCornerShape(20.dp),
                colors = CardDefaults.cardColors(containerColor = teal)
            ) {
                Column(Modifier.fillMaxWidth().padding(18.dp),
                    verticalArrangement = Arrangement.spacedBy(7.dp)) {
                    Text(loc(lang, "UNDERGRADUATE ZOOLOGY", "இளநிலை விலங்கியல்"),
                        fontSize = 11.sp, letterSpacing = 1.sp,
                        color = Color(0xFFD6EEE6), fontWeight = FontWeight.SemiBold)
                    Text("CHORDATA", fontSize = 30.sp, color = Color.White,
                        fontWeight = FontWeight.ExtraBold, letterSpacing = 1.1.sp,
                        modifier = Modifier.testTag("subject-title"))
                    Text(loc(lang, "The Chordata Fieldbook", "முதுகுநாணிகள் கற்றல் களஞ்சியம்"),
                        color = Color.White, fontSize = (16f * scale.coerceAtMost(1.25f)).sp,
                        fontWeight = FontWeight.Medium)
                    Text(
                        loc(lang,
                            "${pack.units.size} units  ·  $total chapters  ·  ${pack.topics.sumOf { it.quiz.size }} questions",
                            "${pack.units.size} அலகுகள்  ·  $total பாடங்கள்  ·  ${pack.topics.sumOf { it.quiz.size }} வினாக்கள்"),
                        color = Color(0xFFE8F7F3), fontSize = 12.sp
                    )
                    Spacer(Modifier.height(2.dp))
                    LinearProgressIndicator(
                        progress = { if (total == 0) 0f else finished.toFloat() / total },
                        color = Color(0xFFF5CE79), trackColor = Color(0xFF5B9990),
                        modifier = Modifier.fillMaxWidth().height(7.dp)
                    )
                    Text(loc(lang, "$finished of $total chapters completed",
                        "$total பாடங்களில் $finished முடிக்கப்பட்டுள்ளன"),
                        fontSize = 12.sp, color = Color.White)
                    Button(
                        onClick = onBrowse, shape = RoundedCornerShape(12.dp),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = Color.White, contentColor = teal),
                        modifier = Modifier.fillMaxWidth()
                    ) { Text(loc(lang, "Explore all lessons", "அனைத்துப் பாடங்களையும் காண்க"),
                        fontWeight = FontWeight.Bold) }
                }
            }
        }
        item(key = "reader-preferences") {
            Card(shape = RoundedCornerShape(14.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White)) {
                Column(Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 8.dp),
                    verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text(loc(lang, "Reading preferences", "வாசிப்பு அமைப்புகள்"),
                        color = ink, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                    Row(verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text(loc(lang, "Language", "மொழி"), fontSize = 12.sp,
                            modifier = Modifier.width(76.dp), color = mutetext)
                        ReadingLanguage.entries.forEach { option ->
                            FilterChip(selected = option == lang, onClick = { onLanguage(option) },
                                label = { Text(if (option == ReadingLanguage.TA) "தமிழ்" else
                                    loc(lang, "English", "ஆங்கிலம்"), fontSize = 12.sp) })
                        }
                    }
                    Row(verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(5.dp)) {
                        Text(loc(lang, "Text size", "எழுத்தளவு"), fontSize = 12.sp,
                            modifier = Modifier.width(76.dp), color = mutetext)
                        Column(verticalArrangement = Arrangement.spacedBy(0.dp)) {
                            listOf(listOf(1f, 1.25f), listOf(1.5f, 2f)).forEach { sizes ->
                                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                    sizes.forEach { option ->
                                        FilterChip(selected = scale == option,
                                            onClick = { onScale(option) },
                                            label = { Text("${(option * 100).toInt()}%",
                                                fontSize = 11.sp) })
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        if (remaining != null) {
            item(key = "continue-reading") {
                Card(onClick = { onOpen(remaining.id) },
                    shape = RoundedCornerShape(14.dp),
                    colors = CardDefaults.cardColors(containerColor = softAmber)) {
                    Row(Modifier.fillMaxWidth().padding(horizontal = 14.dp, vertical = 11.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(3.dp)) {
                            Text(loc(lang, "READ NEXT", "அடுத்துப் படிக்க"),
                                color = accent, fontWeight = FontWeight.Bold, fontSize = 11.sp)
                            BilingualText(remaining.title, lang, scale.coerceAtMost(1.3f),
                                base = 14f, bold = true)
                        }
                        Text("›", color = teal, fontSize = 28.sp)
                    }
                }
            }
        }
        item(key = "units-title") {
            Row(Modifier.fillMaxWidth().padding(top = 4.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically) {
                Text(loc(lang, "Syllabus units", "பாடத்திட்ட அலகுகள்"),
                    fontSize = 19.sp, fontWeight = FontWeight.Bold, color = ink)
                Text(loc(lang, "${pack.units.size} units", "${pack.units.size} அலகுகள்"),
                    color = mutetext, fontSize = 12.sp)
            }
        }
        itemsIndexed(pack.units, key = { _, unit -> unit.id }) { index, unit ->
            val completeInUnit = unit.topics.count { it.id in completed }
            val start = unit.topics.firstOrNull { it.id !in completed }
                ?: unit.topics.first()
            Card(onClick = { onOpen(start.id) }, shape = RoundedCornerShape(14.dp),
                colors = CardDefaults.cardColors(containerColor = unitColours[index % unitColours.size]),
                modifier = Modifier.testTag("home-unit-${unit.id}")) {
                Row(Modifier.fillMaxWidth().padding(12.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    Surface(shape = RoundedCornerShape(10.dp), color = teal) {
                        Text("${index + 1}".padStart(2, '0'), modifier = Modifier.padding(
                            horizontal = 11.dp, vertical = 12.dp), color = Color.White,
                            fontSize = 15.sp, fontWeight = FontWeight.Bold)
                    }
                    Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(3.dp)) {
                        BilingualText(unit.title, lang, scale.coerceAtMost(1.4f),
                            base = 15f, bold = true)
                        Text(loc(lang,
                            "${unit.topics.size} chapters · $completeInUnit completed",
                            "${unit.topics.size} பாடங்கள் · $completeInUnit முடிக்கப்பட்டவை"),
                            fontSize = 12.sp, color = mutetext)
                    }
                    Text("›", fontSize = 24.sp, color = teal)
                }
            }
        }
        item(key = "institution-credit") {
            Text(loc(lang, pack.credit,
                "விலங்கியல் துறை, அரசு கலை மற்றும் அறிவியல் கல்லூரி, நாகர்கோவில்"),
                style = MaterialTheme.typography.labelSmall, color = mutetext,
                modifier = Modifier.fillMaxWidth().padding(vertical = 7.dp),
                textAlign = TextAlign.Center)
        }
    }
}

@Composable
private fun ListingPage(pack: ContentPack, tab: String, query: String, onQuery: (String) -> Unit,
    lang: ReadingLanguage, scale: Float, bookmarks: Set<String>, completed: Set<String>,
    onOpen: (String) -> Unit) {
    val displayed = remember(pack, tab, query, bookmarks) {
        val all = LearningLogic.search(pack, query)
        if (tab == "saved") all.filter { it.id in bookmarks } else all
    }
    LazyColumn(contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(11.dp)) {
        item {
            Text(when (tab) {
                "practice" -> loc(lang, "Practice bank", "வினாப்பயிற்சி")
                "saved" -> loc(lang, "Bookmarks", "சேமித்த பாடங்கள்")
                else -> loc(lang, "All lessons", "அனைத்துப் பாடங்கள்")
            }, fontSize = 22.sp, fontWeight = FontWeight.Bold)
        }
        item {
            OutlinedTextField(query, onQuery,
                label = { Text(loc(lang, "Search lessons", "பாடங்களைத் தேடுக")) }, singleLine = true,
                modifier = Modifier.fillMaxWidth().testTag("lesson-search"))
        }
        if (displayed.isEmpty()) item {
            Text(loc(lang, "No matching topics.", "பொருந்தும் பாடங்கள் இல்லை."), color = mutetext)
        }
        items(displayed, key = { it.id }) { topic ->
            Card(onClick = { onOpen(topic.id) },
                colors = CardDefaults.cardColors(containerColor = Color.White)) {
                Column(Modifier.fillMaxWidth().padding(15.dp), verticalArrangement = Arrangement.spacedBy(5.dp)) {
                    BilingualText(topic.title, lang, scale, base = 15f, bold = true)
                    Text(loc(lang, "${topic.sections.size} lessons · ${topic.quiz.size} questions", "${topic.sections.size} பகுதிகள் · ${topic.quiz.size} வினாக்கள்") +
                        if (topic.id in completed) loc(lang, " · ✓ Complete", " · ✓ முடிந்தது") else "",
                        color = mutetext, fontSize = 12.sp)
                    Text(if (tab == "practice") loc(lang, "Open quiz ›", "வினாப்பயிற்சிக்குச் செல்க ›") else loc(lang, "Read chapter ›", "பாடத்தைப் படிக்க ›"),
                        color = teal, fontWeight = FontWeight.SemiBold)
                }
            }
        }
        item { Spacer(Modifier.height(8.dp)) }
    }
}

@Composable
private fun PointwiseExplanation(points: List<Bilingual>, lang: ReadingLanguage, scale: Float) {
    if (points.isEmpty()) return
    Column(Modifier.fillMaxWidth().testTag("learning-points"),
        verticalArrangement = Arrangement.spacedBy(7.dp)) {
        HorizontalDivider(color = teal.copy(alpha = 0.22f))
        Text(loc(lang, "Key explanations", "முக்கிய விளக்கக் குறிப்புகள்"),
            color = teal, fontWeight = FontWeight.Bold,
            fontSize = (13f * scale.coerceAtMost(1.5f)).sp)
        points.forEachIndexed { number, point ->
            Row(Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.Top,
                horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("${number + 1}.", color = teal,
                    fontWeight = FontWeight.Bold, fontSize = (14f * scale).sp,
                    modifier = Modifier.width(23.dp))
                BilingualText(point, lang, scale, modifier = Modifier.weight(1f),
                    base = 15f, alignment = TextAlign.Start)
            }
        }
    }
}

@Composable
private fun TopicReader(topic: LessonTopic, pack: ContentPack, lang: ReadingLanguage, scale: Float,
    page: Int, onPage: (Int) -> Unit, onNextTopic: () -> Unit,
    onComplete: () -> Unit, completed: Boolean, store: ProgressStore) {
    // Recreate the list position for each lesson page. This avoids briefly showing
    // the previous page's bottom before a LaunchedEffect scroll can execute.
    val listState = key(topic.id, page) { rememberLazyListState() }
    val chapterPages = remember(topic) { LearningLogic.sectionPages(topic) }
    val finalPage = LearningLogic.lastPage(topic)
    var continuous by rememberSaveable(topic.id) { mutableStateOf(false) }
    var outlineExpanded by rememberSaveable(topic.id) { mutableStateOf(false) }
    LaunchedEffect(topic.id, page, continuous) { listState.scrollToItem(0) }
    LazyColumn(state = listState,
        modifier = Modifier.fillMaxSize().background(paper).testTag("lesson-reader-list"),
        contentPadding = PaddingValues(horizontal = 14.dp, vertical = 9.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)) {
        item(key = "breadcrumbs") {
            Text(if (continuous) loc(lang, "CONTINUOUS CHAPTER READING", "தொடர்ச்சியான பாட வாசிப்பு")
                 else loc(lang, "PAGE ${page + 1} OF ${finalPage + 1}", "பக்கம் ${page + 1} / ${finalPage + 1}"),
                color = teal, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            if (!continuous) {
                LinearProgressIndicator(progress = { (page + 1f) / (finalPage + 1f) },
                    modifier = Modifier.fillMaxWidth().padding(top = 4.dp))
            }
        }
        item(key = "heading") {
            BilingualText(if (continuous) topic.title else LearningLogic.title(topic, page), lang, scale,
                modifier = Modifier.padding(vertical = 3.dp).testTag("lesson-page-heading"),
                base = 20f, bold = true)
        }
        if (continuous && page < finalPage) {
            items(topic.sections.size, key = { index -> "chapter-section-${topic.sections[index].key}" }) { index ->
                val section = topic.sections[index]
                Column(verticalArrangement = Arrangement.spacedBy(5.dp)) {
                    Card(
                        shape = RoundedCornerShape(13.dp),
                        colors = CardDefaults.cardColors(
                            containerColor = if (index % 2 == 0) Color.White else softGreen)
                    ) {
                        Column(Modifier.fillMaxWidth().padding(13.dp),
                            verticalArrangement = Arrangement.spacedBy(7.dp)) {
                            Text(loc(lang, "SECTION ${index + 1}", "பகுதி ${index + 1}"),
                                fontSize = 11.sp, color = teal, fontWeight = FontWeight.Bold)
                            BilingualText(section.heading, lang, scale,
                                base = 18f, bold = true)
                            BilingualText(section.body, lang, scale,
                                modifier = Modifier.fillMaxWidth(),
                                base = 16f, alignment = TextAlign.Start)
                            PointwiseExplanation(section.keyPoints, lang, scale)
                        }
                    }
                    // Every illustration stays immediately after its exact
                    // registered lesson section; original manifest mapping is unchanged.
                    FigureGallery(topic.id, index + 1, lang, topic.diagramIds.size)
                }
            }
        } else when {
            page < chapterPages.size -> {
                // A book page can contain more than one brief lesson section.
                // Section order, illustrations and academic content are unchanged.
                if (page == 0) {
                    item(key = "chapter-guide") {
                        Card(shape = RoundedCornerShape(13.dp),
                            colors = CardDefaults.cardColors(containerColor = softGreen)) {
                            Column(Modifier.fillMaxWidth().padding(12.dp),
                                verticalArrangement = Arrangement.spacedBy(5.dp)) {
                                Text(
                                    loc(lang, "CHAPTER GUIDE · ${topic.sections.size} sections · ${topic.quiz.size} questions",
                                        "பாட வழிகாட்டி · ${topic.sections.size} பகுதிகள் · ${topic.quiz.size} வினாக்கள்"),
                                    color = teal, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                                Row(Modifier.fillMaxWidth(),
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                    OutlinedButton(
                                        onClick = { outlineExpanded = !outlineExpanded },
                                        modifier = Modifier.weight(1f).heightIn(min = 42.dp)
                                            .testTag("chapter-outline-toggle")) {
                                        Text(if (outlineExpanded)
                                            loc(lang, "Hide outline", "பாட அமைப்பை மறை")
                                        else loc(lang, "View outline", "பாட அமைப்பைக் காண்க"),
                                            maxLines = 2, textAlign = TextAlign.Center)
                                    }
                                    Button(onClick = { continuous = true },
                                        modifier = Modifier.weight(1f).heightIn(min = 42.dp)
                                            .testTag("read-full-chapter")) {
                                        Text(loc(lang, "Read continuously", "தொடர்ந்து படிக்க"),
                                            maxLines = 2, textAlign = TextAlign.Center)
                                    }
                                }
                                if (outlineExpanded) {
                                    topic.sections.forEachIndexed { index, section ->
                                        Text("${index + 1}. " +
                                            (if (lang == ReadingLanguage.TA)
                                                section.heading.ta else section.heading.en),
                                            fontSize = (13f * scale.coerceAtMost(1.5f)).sp,
                                            lineHeight = (19f * scale.coerceAtMost(1.5f)).sp)
                                    }
                                }
                            }
                        }
                    }
                }
                chapterPages[page].forEach { sectionIndex ->
                    item(key = "section-body-${sectionIndex}") {
                        val section = topic.sections[sectionIndex]
                        val sectionColour = if (section.key.contains("definition") ||
                            section.key.contains("characters")) softGreen else
                            if (sectionIndex % 2 == 0) Color.White else paper
                        Card(shape = RoundedCornerShape(12.dp),
                            colors = CardDefaults.cardColors(containerColor = sectionColour)) {
                            Column(Modifier.fillMaxWidth().padding(13.dp),
                                verticalArrangement = Arrangement.spacedBy(9.dp)) {
                                // Page heading identifies the first section; later
                                // packed sections get their own visible subheadings.
                                if (page == 0 || sectionIndex != chapterPages[page].first()) {
                                    BilingualText(section.heading, lang, scale,
                                        base = 18f, bold = true,
                                        modifier = Modifier.testTag(if (sectionIndex == 0)
                                            "first-section-heading"
                                        else "packed-section-heading-${sectionIndex}"))
                                }
                                BilingualText(section.body, lang, scale,
                                    modifier = Modifier.fillMaxWidth(),
                                    base = 16f, alignment = TextAlign.Start)
                                PointwiseExplanation(section.keyPoints, lang, scale)
                            }
                        }
                    }
                    // Register indices remain one-based by the ORIGINAL section,
                    // independent of how multiple sections share a visible page.
                    item(key = "section-figures-${sectionIndex}") {
                        FigureGallery(topic.id, sectionIndex + 1, lang, topic.diagramIds.size)
                    }
                }
            }
            else -> {
                item(key = "quiz") {
                    QuizPage(topic, lang, scale, store, onComplete)
                }
            }
        }
        item(key = "pager") {
            HorizontalDivider()
            if (continuous && page < finalPage) {
                // At enlarged text sizes, long bilingual reading-mode actions
                // require full-width controls rather than squeezed buttons.
                if (scale >= 1.5f) {
                    Column(Modifier.fillMaxWidth().padding(top = 7.dp),
                        verticalArrangement = Arrangement.spacedBy(7.dp)) {
                        OutlinedButton(onClick = { continuous = false; onPage(0) },
                            modifier = Modifier.fillMaxWidth().heightIn(min = 48.dp)) {
                            Text(loc(lang, "Page-by-page", "பக்கங்களாகப் படிக்க"),
                                textAlign = TextAlign.Center)
                        }
                        Button(onClick = { continuous = false; onPage(finalPage) },
                            modifier = Modifier.fillMaxWidth().heightIn(min = 48.dp)) {
                            Text(loc(lang, "Practice questions ›", "வினாப்பயிற்சி ›"),
                                textAlign = TextAlign.Center)
                        }
                    }
                } else {
                    Row(modifier = Modifier.fillMaxWidth().padding(top = 7.dp),
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalAlignment = Alignment.CenterVertically) {
                        OutlinedButton(onClick = { continuous = false; onPage(0) },
                            modifier = Modifier.weight(1f).heightIn(min = 48.dp)) {
                            Text(loc(lang, "Page-by-page", "பக்கங்களாகப் படிக்க"),
                                maxLines = 2, textAlign = TextAlign.Center)
                        }
                        Button(onClick = { continuous = false; onPage(finalPage) },
                            modifier = Modifier.weight(1f).heightIn(min = 48.dp)) {
                            Text(loc(lang, "Practice questions ›", "வினாப்பயிற்சி ›"),
                                maxLines = 2, textAlign = TextAlign.Center)
                        }
                    }
                }
            } else {
                // Page numbers already appear in the progress header. A second
                // central counter forced Tamil navigation into vertical strips
                // on 320dp emulators. Give both actions equal, usable widths.
                Row(modifier = Modifier.fillMaxWidth().padding(top = 7.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalAlignment = Alignment.CenterVertically) {
                    OutlinedButton(onClick = { onPage(LearningLogic.pageBefore(page)) },
                        enabled = page > 0,
                        modifier = Modifier.weight(1f).heightIn(min = 48.dp)
                            .testTag("reader-previous")) {
                        Text(loc(lang, "‹ Previous", "‹ முந்தையது"),
                            maxLines = 2, textAlign = TextAlign.Center)
                    }
                    Button(onClick = { if (page < finalPage) onPage(page + 1) else onNextTopic() },
                        enabled = page < finalPage || LearningLogic.nextTopic(pack, topic.id) != null,
                        modifier = Modifier.weight(1f).heightIn(min = 48.dp)
                            .testTag("reader-next")) {
                        Text(if (page < finalPage) loc(lang, "Next ›", "அடுத்து ›")
                            else loc(lang, "Next topic ›", "அடுத்த பாடம் ›"),
                            maxLines = 2, textAlign = TextAlign.Center)
                    }
                }
            }
            if (completed) Text(loc(lang, "✓ Chapter completed", "✓ பாடம் முடிக்கப்பட்டது"),
                color = teal, modifier = Modifier.padding(top = 5.dp))
        }
    }
}

@Composable
private fun QuizPage(topic: LessonTopic, lang: ReadingLanguage, scale: Float,
    store: ProgressStore, onComplete: () -> Unit) {
    // All answers are in-memory until submission, then the score and completion are persisted.
    val answerSaver = listSaver<SnapshotStateList<Int>, Int>(
        save = { it.toList() }, restore = { it.toMutableStateList() }
    )
    val answers: SnapshotStateList<Int> = rememberSaveable(topic.id, saver = answerSaver) {
        mutableStateListOf<Int>().apply { repeat(topic.quiz.size) { add(-1) } }
    }
    var submitted by rememberSaveable(topic.id) { mutableStateOf(false) }
    Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
        topic.quiz.forEachIndexed { index, question ->
            Card(colors = CardDefaults.cardColors(containerColor = Color.White)) {
                Column(Modifier.fillMaxWidth().padding(14.dp), verticalArrangement = Arrangement.spacedBy(11.dp)) {
                    Text(loc(lang, "QUESTION ${index + 1} / ${topic.quiz.size}", "வினா ${index + 1} / ${topic.quiz.size}"), fontSize = 12.sp,
                        color = teal, fontWeight = FontWeight.Bold)
                    BilingualText(question.question, lang, scale, base = 16f, bold = true)
                    question.options.forEachIndexed { optionIndex, option ->
                        Row(Modifier.fillMaxWidth()
                            .clickable(enabled = !submitted) { answers[index] = optionIndex }
                            .padding(vertical = 5.dp),
                            verticalAlignment = Alignment.Top) {
                            RadioButton(selected = answers[index] == optionIndex,
                                onClick = { if (!submitted) answers[index] = optionIndex },
                                enabled = !submitted)
                            BilingualText(option, lang, scale, modifier = Modifier.weight(1f)
                                .padding(top = 10.dp), base = 14f)
                        }
                    }
                    if (submitted) {
                        HorizontalDivider()
                        Text(if (answers[index] == question.correctIndex) loc(lang, "✓ Correct", "✓ சரி") else
                            loc(lang, "Correct option: ${question.correctIndex + 1}", "சரியான விடை: ${question.correctIndex + 1}"),
                            color = if (answers[index] == question.correctIndex) teal else accent,
                            fontWeight = FontWeight.Bold)
                        BilingualText(question.explanation, lang, scale, base = 14f)
                    }
                }
            }
        }
        if (!submitted) {
            Button(onClick = {
                submitted = true
                val score = LearningLogic.score(answers.toList(), topic.quiz)
                store.saveQuizScore(topic.id, score)
                onComplete()
            }, enabled = answers.all { it in 0..3 }, modifier = Modifier.fillMaxWidth()) {
                Text(loc(lang, "Submit answers", "விடைகளைச் சமர்ப்பி"))
            }
        } else {
            val score = LearningLogic.score(answers.toList(), topic.quiz)
            Text(loc(lang, "Score: $score / ${topic.quiz.size}", "மதிப்பெண்: $score / ${topic.quiz.size}"), fontSize = 19.sp, fontWeight = FontWeight.Bold,
                color = teal)
            OutlinedButton(onClick = {
                answers.indices.forEach { answers[it] = -1 }
                submitted = false
            }) { Text(loc(lang, "Try again", "மீண்டும் முயற்சி")) }
        }
    }
}

@Composable
fun ErrorContent(message: String, lang: ReadingLanguage) {
    MaterialTheme(colorScheme = scheme) {
        Column(Modifier.fillMaxSize().padding(24.dp),
            verticalArrangement = Arrangement.Center) {
            Text(loc(lang, "Offline content unavailable", "இணையமற்ற பாட உள்ளடக்கம் கிடைக்கவில்லை"),
                fontSize = 22.sp, fontWeight = FontWeight.Bold)
            Text(loc(lang, message, "பாடத் தரவைக் திறக்க இயலவில்லை."), color = mutetext)
            Text(loc(lang, "Please reopen the lesson after checking the installation.",
                "பாடங்களைத் திறக்க நிறுவலைச் சரிபார்க்கவும்."), color = accent)
        }
    }
}
