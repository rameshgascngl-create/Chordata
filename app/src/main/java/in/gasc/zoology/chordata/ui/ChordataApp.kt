package `in`.gasc.zoology.chordata.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bookmark
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
                            Text(if (currentTopic == null) "CHORDATA  ·  ATLAS" else "CHORDATA",
                                style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                            Text(if (currentTopic == null) "B.Sc. Zoology • Offline" else
                                currentTopic.title.en,
                                maxLines = 1, overflow = TextOverflow.Ellipsis,
                                style = MaterialTheme.typography.labelSmall, color = mutetext)
                        }
                    },
                    navigationIcon = {
                        if (currentTopic != null) TextButton(onClick = { selectedTopicId = "" }) {
                            Text("‹ Back", fontSize = 15.sp)
                        }
                    },
                    actions = {
                        if (currentTopic != null) {
                            IconButton(onClick = { updateBookmarks(currentTopic.id) },
                                modifier = Modifier.size(48.dp)) {
                                Icon(Icons.Default.Bookmark, contentDescription = if (currentTopic.id in bookmarks)
                                    "Remove bookmark" else "Save bookmark",
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
    Column(modifier, verticalArrangement = Arrangement.spacedBy(5.dp)) {
        if (lang != ReadingLanguage.TA) {
            Text(value.en, fontSize = (base * scale).sp, lineHeight = (base * scale * 1.48f).sp,
                fontWeight = if (bold) FontWeight.SemiBold else FontWeight.Normal)
        }
        if (lang != ReadingLanguage.EN) {
            Text(value.ta, fontSize = (base * scale).sp, lineHeight = (base * scale * 1.55f).sp,
                fontWeight = if (bold) FontWeight.SemiBold else FontWeight.Normal,
                color = if (lang == ReadingLanguage.BOTH) teal else ink)
        }
    }
}

@Composable
private fun HomePage(pack: ContentPack, lang: ReadingLanguage, scale: Float,
    completed: Set<String>, bookmarks: Set<String>, onLanguage: (ReadingLanguage) -> Unit,
    onScale: (Float) -> Unit, onOpen: (String) -> Unit, onBrowse: () -> Unit) {
    LazyColumn(contentPadding = PaddingValues(16.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        item {
            ElevatedCard(colors = CardDefaults.elevatedCardColors(containerColor = teal)) {
                Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(9.dp)) {
                    Text("The Chordata Fieldbook", color = Color.White, fontWeight = FontWeight.Bold,
                        fontSize = 22.sp)
                    Text("முதுகுநாணிகள் கற்றல் களஞ்சியம்", color = Color.White, fontSize = 18.sp)
                    Text("Five units · 39 topics · 117 questions", color = Color.White)
                    LinearProgressIndicator(progress = { completed.size.toFloat() / pack.topics.size },
                        color = Color(0xFFF5CF6A), trackColor = Color(0xFF59948E),
                        modifier = Modifier.fillMaxWidth().height(6.dp))
                    Text("${completed.size} of ${pack.topics.size} topics completed",
                        color = Color.White)
                    Button(onClick = onBrowse, colors = ButtonDefaults.buttonColors(containerColor = Color.White,
                        contentColor = teal)) { Text("Explore all lessons") }
                }
            }
        }
        item {
            Text("Reading language  /  மொழி", style = MaterialTheme.typography.titleSmall)
            Spacer(Modifier.height(6.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.fillMaxWidth()) {
                ReadingLanguage.entries.forEach { option ->
                    FilterChip(selected = option == lang, onClick = { onLanguage(option) },
                        label = { Text(when (option) {
                            ReadingLanguage.EN -> "English"
                            ReadingLanguage.TA -> "தமிழ்"
                            ReadingLanguage.BOTH -> "Both"
                        }, fontSize = 12.sp) })
                }
            }
            Text("Text magnification  /  எழுத்தளவு", style = MaterialTheme.typography.titleSmall)
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
        item { Text("Syllabus units", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold) }
        items(pack.units, key = { it.id }) { unit ->
            Card(onClick = { onOpen(unit.topics.first().id) },
                colors = CardDefaults.cardColors(containerColor = Color.White)) {
                Column(Modifier.padding(16.dp).fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    BilingualText(unit.title, lang, scale, base = 15f, bold = true)
                    Text("${unit.topics.size} topics · ${unit.topics.count { it.id in completed }} completed",
                        color = mutetext)
                    Text("Open first topic  ›", color = teal, fontWeight = FontWeight.SemiBold)
                }
            }
        }
        item {
            Text("Figures: 64 awaiting verification · No unapproved images inserted.",
                style = MaterialTheme.typography.bodySmall, color = mutetext)
            Text("${bookmarks.size} bookmarked chapters · progress stored on this device",
                style = MaterialTheme.typography.bodySmall, color = mutetext)
            Text(pack.credit, style = MaterialTheme.typography.labelSmall, color = mutetext)
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
                "practice" -> "Practice bank / வினாப்பயிற்சி"
                "saved" -> "Bookmarks / சேமித்த பாடங்கள்"
                else -> "All lessons / அனைத்துப் பாடங்கள்"
            }, fontSize = 22.sp, fontWeight = FontWeight.Bold)
        }
        item {
            OutlinedTextField(query, onQuery,
                label = { Text("Search in English or Tamil") }, singleLine = true,
                modifier = Modifier.fillMaxWidth())
        }
        if (displayed.isEmpty()) item {
            Text("No matching topics. / பொருந்தும் பாடங்கள் இல்லை.", color = mutetext)
        }
        items(displayed, key = { it.id }) { topic ->
            Card(onClick = { onOpen(topic.id) },
                colors = CardDefaults.cardColors(containerColor = Color.White)) {
                Column(Modifier.fillMaxWidth().padding(15.dp), verticalArrangement = Arrangement.spacedBy(5.dp)) {
                    BilingualText(topic.title, lang, scale, base = 15f, bold = true)
                    Text("${topic.sections.size} lessons · ${topic.quiz.size} questions" +
                        if (topic.id in completed) " · ✓ Complete" else "",
                        color = mutetext, fontSize = 12.sp)
                    Text(if (tab == "practice") "Open quiz  ›" else "Read chapter  ›",
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
            Text("${topic.id.uppercase()}  •  PAGE ${page + 1} OF ${finalPage + 1}",
                color = teal, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            LinearProgressIndicator(progress = { (page + 1f) / (finalPage + 1f) },
                modifier = Modifier.fillMaxWidth().padding(top = 7.dp))
        }
        item(key = "heading") {
            BilingualText(LearningLogic.title(topic, page), lang, scale, base = 20f, bold = true)
        }
        when {
            page == 0 -> {
                item {
                    Card(colors = CardDefaults.cardColors(containerColor = pale)) {
                        Column(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                            Text("Chapter outline  /  பாட அமைப்பு", fontWeight = FontWeight.Bold,
                                color = teal)
                            topic.sections.forEachIndexed { i, section ->
                                Text("${i + 1}. ${if (lang == ReadingLanguage.TA) section.heading.ta else section.heading.en}",
                                    fontSize = (14f * scale).sp, lineHeight = (21f * scale).sp)
                            }
                            Text("Quiz: ${topic.quiz.size} questions", color = mutetext)
                        }
                    }
                }
                item {
                    if (topic.diagramIds.isNotEmpty()) {
                        Card(colors = CardDefaults.cardColors(containerColor = Color(0xFFFFF5E8))) {
                            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                Text("Illustrations pending approval / படங்களுக்கான ஒப்புதல் நிலுவையில் உள்ளது",
                                    fontWeight = FontWeight.Bold, color = accent)
                                Text("${topic.diagramIds.size} diagram references. Only approved, attributed, scientifically reviewed plates will be displayed.",
                                    color = mutetext)
                                topic.diagramIds.forEach { id -> Text("• $id", color = mutetext, fontSize = 12.sp) }
                            }
                        }
                    }
                }
            }
            page <= topic.sections.size -> {
                item(key = "section-body") {
                    BilingualText(topic.sections[page - 1].body, lang, scale, base = 16f)
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
                    enabled = page > 0) { Text("‹ Prev") }
                Text("${page + 1} / ${finalPage + 1}", fontWeight = FontWeight.SemiBold)
                Button(onClick = { if (page < finalPage) onPage(page + 1) else onNextTopic() },
                    enabled = page < finalPage || LearningLogic.nextTopic(pack, topic.id) != null) {
                    Text(if (page < finalPage) "Next ›" else "Next topic ›")
                }
            }
            if (completed) Text("✓ Chapter completed", color = teal,
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
                    Text("QUESTION ${index + 1} / ${topic.quiz.size}", fontSize = 12.sp,
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
                        Text(if (answers[index] == question.correctIndex) "✓ Correct / சரி" else
                            "Correct option: ${question.correctIndex + 1} / சரியான விடை: ${question.correctIndex + 1}",
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
                Text("Submit answers  /  விடைகளைச் சமர்ப்பி")
            }
        } else {
            val score = LearningLogic.score(answers.toList(), topic.quiz)
            Text("Score: $score / ${topic.quiz.size}", fontSize = 19.sp, fontWeight = FontWeight.Bold,
                color = teal)
            OutlinedButton(onClick = {
                answers.indices.forEach { answers[it] = -1 }
                submitted = false
            }) { Text("Try again / மீண்டும் முயற்சி") }
        }
    }
}

@Composable
fun ErrorContent(message: String) {
    MaterialTheme(colorScheme = scheme) {
        Column(Modifier.fillMaxSize().padding(24.dp),
            verticalArrangement = Arrangement.Center) {
            Text("Offline content unavailable", fontSize = 22.sp, fontWeight = FontWeight.Bold)
            Text(message, color = mutetext)
            Text("The app will not substitute incomplete or unverified lessons.", color = accent)
        }
    }
}
