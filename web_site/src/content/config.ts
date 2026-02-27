// web_site/src/content/config.ts
import { z, defineCollection } from 'astro:content';

const charactersCollection = defineCollection({
  type: 'data',
  schema: z.object({
    id: z.string(),
    characterName: z.string(),
    identityName: z.string(),
    isDefault: z.boolean(),
    grade: z.number(), 
    releaseDate: z.string(),
    keywords: z.array(z.string()),
    
    // 공격 유형과 죄악 속성을 묶어서 관리
    skills: z.object({
      skill1: z.object({ type: z.string(), attribute: z.string() }),
      skill2: z.object({ type: z.string(), attribute: z.string() }),
      skill3: z.object({ type: z.string(), attribute: z.string() }),
      special1: z.object({ type: z.string(), attribute: z.string() }).optional(),
      special2: z.object({ type: z.string(), attribute: z.string() }).optional(),
      special3: z.object({ type: z.string(), attribute: z.string() }).optional(),
    }),
    
    // 수비 스킬도 속성을 가질 수 있도록 객체로 변경
    defense: z.object({ type: z.string(), attribute: z.string() }),
    
    affiliation: z.array(z.string()), 
    image_url: z.string(),
  }),
});

export const collections = { 'characters': charactersCollection };