SELECT
	"INSTANCE"."INSTANCE_ID",
	"ANSWER_DOK_NR"."ANSWER"   AS "DOSSIER_NR",
	"FORM"."NAME"              AS "FORM",
	TO_CHAR("ACTIVATION"."DEADLINE_DATE", 'DD.MM.YYYY') AS "DEADLINE",
	"LOCATION"."NAME"          AS "COMMUNITY",
	(SELECT LISTAGG("ANSWER", ', ') WITHIN GROUP (ORDER BY "QUESTION_ID" DESC)
		FROM
			"ANSWER"
		WHERE
			"INSTANCE"."INSTANCE_ID" = "ANSWER"."INSTANCE_ID"
			AND
			(
				"ANSWER"."QUESTION_ID" = 23
				OR
				"ANSWER"."QUESTION_ID" = 221
			)
			AND
			"ANSWER"."CHAPTER_ID" = 1
			AND
			"ANSWER"."ITEM" = 1
	) AS "APPLICANT",
	(SELECT LISTAGG("NAME", ', ') WITHIN GROUP (ORDER BY "NAME") 
		FROM INTENTIONS WHERE "INSTANCE_ID" = "INSTANCE"."INSTANCE_ID") AS "INTENT",
	CASE
		WHEN "ANSWER_STREET_BG"."ANSWER" IS NOT NULL THEN "ANSWER_STREET_BG"."ANSWER"
		WHEN "ANSWER_STREET_NP"."ANSWER" IS NOT NULL THEN "ANSWER_STREET_NP"."ANSWER"
	END AS "STREET",
	"ACTIVATION"."REASON"      AS "REASON",
	"INSTANCE_STATE"."NAME"    AS "STATE",
	"INSTANCE_STATE_DESCRIPTION"."DESCRIPTION"    AS "STATE_DESCRIPTION"
FROM
	"INSTANCE"
JOIN
	"INSTANCE_LOCATION" ON (
		"INSTANCE"."INSTANCE_ID" = "INSTANCE_LOCATION"."INSTANCE_ID"
	)

JOIN
	"LOCATION" ON (
	 "INSTANCE_LOCATION"."LOCATION_ID" = "LOCATION"."LOCATION_ID"
	)

JOIN
	FORM ON (
		"INSTANCE"."FORM_ID" = "FORM"."FORM_ID"
)

LEFT JOIN
	"ANSWER" "ANSWER_DOK_NR" ON (
		"INSTANCE"."INSTANCE_ID" = "ANSWER_DOK_NR"."INSTANCE_ID"
		AND
		"ANSWER_DOK_NR"."QUESTION_ID" = 6
		AND
		"ANSWER_DOK_NR"."CHAPTER_ID" = 2
		AND
		"ANSWER_DOK_NR"."ITEM" = 1
	)

LEFT JOIN
	"ANSWER" "ANSWER_STREET_BG" ON (
		"INSTANCE"."INSTANCE_ID" = "ANSWER_STREET_BG"."INSTANCE_ID"
		AND
		"ANSWER_STREET_BG"."QUESTION_ID" = 93
		AND
		"ANSWER_STREET_BG"."CHAPTER_ID" = 21
		AND
		"ANSWER_STREET_BG"."ITEM" = 1
	)

LEFT JOIN
	"ANSWER" "ANSWER_STREET_NP" ON (
		"INSTANCE"."INSTANCE_ID" = "ANSWER_STREET_NP"."INSTANCE_ID"
		AND
		"ANSWER_STREET_NP"."QUESTION_ID" = 93
		AND
		"ANSWER_STREET_NP"."CHAPTER_ID" = 101
		AND
		"ANSWER_STREET_NP"."ITEM" = 1
	)

JOIN
	"INSTANCE_STATE" ON (
	"INSTANCE_STATE"."NAME" = 'circ'
)

LEFT JOIN
	"INSTANCE_STATE_DESCRIPTION" ON (
		"INSTANCE_STATE_DESCRIPTION"."INSTANCE_STATE_ID" = "INSTANCE_STATE"."INSTANCE_STATE_ID"
	)

JOIN
	"CIRCULATION" ON (
		"CIRCULATION"."INSTANCE_ID" = "INSTANCE"."INSTANCE_ID"
	)

JOIN
	"ACTIVATION" ON (
		"ACTIVATION"."CIRCULATION_ID" = "CIRCULATION"."CIRCULATION_ID"
		AND
		"ACTIVATION"."SERVICE_ID" = [SERVICE_ID]
	)

WHERE
	"INSTANCE"."INSTANCE_STATE_ID" = "INSTANCE_STATE"."INSTANCE_STATE_ID"
	AND
	"ACTIVATION"."CIRCULATION_STATE_ID" = 1
