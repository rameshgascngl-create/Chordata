package `in`.gasc.zoology.chordata.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
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
private val scheme = lightColorScheme(primary = teal, secondary = accent,
    background = Color(0xFFF7FAFA), surface = Color.White, onSurface = ink)

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
                NavigationBar(containerColor = Color.White) {
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
    modifier: Modifier = Modifier, base: Float = 16f, bold: Boolean = false) {
    Text(
        if (lang == ReadingLanguage.TA) value.ta else value.en,
        modifier = modifier,
        fontSize = (base * scale).sp,
        lineHeight = (base * scale * if (lang == ReadingLanguage.TA) 1.55f else 1.48f).sp,
        fontWeight = if (bold) FontWeight.SemiBold else FontWeight.Normal
    )
}

@Composable
private fun HomePage(pack: ContentPack, lang: ReadingLanguage, scale: Float,
    completed: Set<String>, bookmarks: Set<String>, onLanguage: (ReadingLanguage) -> Unit,
    onScale: (Float) -> Unit, onOpen: (String) -> Unit, onBrowse: () -> Unit) {
    LazyColumn(contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        item {
            ElevatedCard(colors = CardDefaults.elevatedCardColors(containerColor = teal)) {
                Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(9.dp)) {
                    Text(loc(lang, "The Chordata Fieldbook", "முதுகுநாணிகள் கற்றல் களஞ்சியம்"), color = Color.White, fontWeight = FontWeight.Bold, fontSize = 22.sp)
                    Text(loc(lang, "Five units · 39 topics · 117 questions", "ஐந்து அலகுகள் · 39 பாடங்கள் · 117 வினாக்கள்"), color = Color.White)
                    LinearProgressIndicator(progress = { completed.size.toFloat() / pack.topics.size },
                        color = Color(0xFFF5CF6A), trackColor = Color(0xFF59948E),
                        modifier = Modifier.fillMaxWidth().height(6.dp))
                    Text(loc(lang, "${completed.size} of ${pack.topics.size} topics completed", "${pack.topics.size} பாடங்களில் ${completed.size} முடிக்கப்பட்டுள்ளன"),
                        color = Color.White)
                    Button(onClick = onBrowse, colors = ButtonDefaults.buttonColors(containerColor = Color.White,
                        contentColor = teal)) { Text(loc(lang, "Explore all lessons", "அனைத்துப் பாடங்களையும் காண்க")) }
                }
            }
        }
        item {
            Text(loc(lang, "Reading language", "பயிற்றுமொழி"), style = MaterialTheme.typography.titleSmall)
            Spacer(Modifier.height(6.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.fillMaxWidth()) {
                ReadingLanguage.entries.forEach { option ->
                    FilterChip(selected = option == lang, onClick = { onLanguage(option) },
                        label = { Text(when (option) {
                            ReadingLanguage.EN -> loc(lang, "English", "ஆங்கிலம்")
                            ReadingLanguage.TA -> "தமிழ்"
                                                    }, fontSize = 12.sp) })
                }
            }
            Text(loc(lang, "Text magnification", "எழுத்தளவு"), style = MaterialTheme.typography.titleSmall)
            Column {
                listOf(listOf(1f, 1.25f), listOf(1.5f, 2f)).forEach { sizes ->
                    Row(horizontalArrangement = Arrangement.spacedBy(7.dp)) {
                        sizes.forEach { size ->
                            FilterChip(selected = scale == size, onClick = { onScale(size) },
                                label = { Text("${(size * 100).toInt()}%") })
                        }
                    }
                }
            }
        }
        item { Text(loc(lang, "Syllabus units", "பாடத்திட்ட அலகுகள்"), style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold) }
        items(pack.units, key = { it.id }) { unit ->
            Card(onClick = { onOpen(unit.topics.first().id) },
                colors = CardDefaults.cardColors(containerColor = Color.White)) {
                Column(Modifier.padding(16.dp).fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    BilingualText(unit.title, lang, scale, base = 15f, bold = true)
                    Text(loc(lang, "${unit.topics.size} topics · ${unit.topics.count { it.id in completed }} completed", "${unit.topics.size} பாடங்கள் · ${unit.topics.count { it.id in completed }} முடிக்கப்பட்டவை"),
                        color = mutetext)
                    Text(loc(lang, "Open first topic ›", "முதல் பாடத்திற்குச் செல்க ›"), color = teal, fontWeight = FontWeight.SemiBold)
                }
            }
        }
        item {
            Text(loc(lang, "Three reference illustrations are available in English and Tamil. Additional anatomical plates remain under review.", "மூன்று ஆதார வரைபடங்கள் தமிழ், ஆங்கிலப் பதிப்புகளில் உள்ளன. பிற உடற்கூறியல் படங்கள் சரிபார்ப்பில் உள்ளன."),
                style = MaterialTheme.typography.bodySmall, color = mutetext)
            Text(loc(lang, "${bookmarks.size} bookmarked chapters · progress stored on this device", "${bookmarks.size} சேமித்த பாடங்கள் · கற்றல் முன்னேற்றம் இக்கருவியில் சேமிக்கப்படுகிறது"),
                style = MaterialTheme.typography.bodySmall, color = mutetext)
            Text(loc(lang, pack.credit, "விலங்கியல் துறை, அரசு கலை மற்றும் அறிவியல் கல்லூரி, நாகர்கோவில் · உருவாக்கம்: இரா. ரமேஷ்"), style = MaterialTheme.typography.labelSmall, color = mutetext)
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
private fun TopicReader(topic: LessonTopic, pack: ContentPack, lang: ReadingLanguage, scale: Float,
    page: Int, onPage: (Int) -> Unit, onNextTopic: () -> Unit,
    onComplete: () -> Unit, completed: Boolean, store: ProgressStore) {
    // Recreate the list position for each lesson page. This avoids briefly showing
    // the previous page's bottom before a LaunchedEffect scroll can execute.
    val listState = key(topic.id, page) { rememberLazyListState() }
    LaunchedEffect(topic.id, page) { listState.scrollToItem(0) }
    val finalPage = LearningLogic.lastPage(topic)
    LazyColumn(state = listState, modifier = Modifier.fillMaxSize().testTag("lesson-reader-list"),
        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 15.dp),
        verticalArrangement = Arrangement.spacedBy(15.dp)) {
        item(key = "breadcrumbs") {
            Text(loc(lang, "PAGE ${page + 1} OF ${finalPage + 1}", "பக்கம் ${page + 1} / ${finalPage + 1}"),
                color = teal, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            LinearProgressIndicator(progress = { (page + 1f) / (finalPage + 1f) },
                modifier = Modifier.fillMaxWidth().padding(top = 7.dp))
        }
        item(key = "heading") {
            BilingualText(LearningLogic.title(topic, page), lang, scale,
                modifier = Modifier.testTag("lesson-page-heading"), base = 20f, bold = true)
        }
        when {
            page == 0 -> {
                item {
                    Card(colors = CardDefaults.cardColors(containerColor = pale)) {
                        Column(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            Text(loc(lang, "Chapter outline", "பாட அமைப்பு"), fontWeight = FontWeight.Bold,
                                color = teal)
                            topic.sections.forEachIndexed { i, section ->
                                Text("${i + 1}. ${if (lang == ReadingLanguage.TA) section.heading.ta else section.heading.en}",
                                    fontSize = (14f * scale).sp, lineHeight = (21f * scale).sp)
                            }
                            Text(loc(lang, "Quiz: ${topic.quiz.size} questions", "வினாப்பயிற்சி: ${topic.quiz.size} வினாக்கள்"), color = mutetext)
                        }
                    }
                }
                item(key = "intro-figures") { FigureGallery(topic.id, 0, lang, topic.diagramIds.size) }

            }
            page <= topic.sections.size -> {
                item(key = "section-body") {
                    BilingualText(topic.sections[page - 1].body, lang, scale, base = 16f)
                    FigureGallery(topic.id, page, lang, topic.diagramIds.size)
                }
            }
            else -> {
                item(key = "quiz") {
                    QuizPage(topic, lang, scale, store, onComplete)
                }
            }
        }
        item(key = "pager") {
            Spacer(Modifier.height(16.dp))
            HorizontalDivider()
            Row(modifier = Modifier.fillMaxWidth().padding(top = 12.dp),
                horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                OutlinedButton(onClick = { onPage(LearningLogic.pageBefore(page)) },
                    enabled = page > 0) { Text(loc(lang, "‹ Previous", "‹ முந்தையது")) }
                Text(loc(lang, "${page + 1} / ${finalPage + 1}", "பக்கம் ${page + 1} / ${finalPage + 1}"), fontWeight = FontWeight.SemiBold)
                Button(onClick = { if (page < finalPage) onPage(page + 1) else onNextTopic() },
                    enabled = page < finalPage || LearningLogic.nextTopic(pack, topic.id) != null) {
                    Text(if (page < finalPage) loc(lang, "Next ›", "அடுத்து ›") else loc(lang, "Next topic ›", "அடுத்த பாடம் ›"))
                }
            }
            if (completed) Text(loc(lang, "✓ Chapter completed", "✓ பாடம் முடிக்கப்பட்டது"), color = teal,
                modifier = Modifier.padding(top = 10.dp))
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
            Text(loc(lang, "The app will not substitute incomplete or unverified lessons.",
                "சரிபார்க்கப்படாத பாடங்கள் மாற்றாக வழங்கப்படமாட்டா."), color = accent)
        }
    }
}
