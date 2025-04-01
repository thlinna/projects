const { OpenAI } = require('openai');

// Luo OpenAI-instanssi
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

/**
 * Luo vastauksen tekoälymallista käyttämällä käyttäjän syötettä
 * @param {string} role - Agentin rooli (ideanikkari, arvioija, hakija, rahoittaja)
 * @param {string} prompt - Käyttäjän syöte
 * @param {object} data - Mahdolliset lisätiedot
 * @returns {Promise<string>} Tekoälyn vastaus
 */
exports.createCompletion = async (role, prompt, data = {}) => {
  try {
    // Määrittele systeemin ohjeistus agentin roolille
    let systemInstruction = '';
    
    switch (role) {
      case 'ideanikkari':
        systemInstruction = 
          'Olet Ideanikkari, tekoälyagentti, joka auttaa ideoimaan innovatiivisia rahoitushakemuksia Digital Europe Program -rahoitusohjelmaan. ' +
          'Tehtäväsi on luoda luovia, toteutettavissa olevia ideoita, jotka sopivat ohjelman painopistealueisiin. ' +
          'Keskity erityisesti tekoälyn, kyberturvallisuuden, digitaalisten taitojen ja osaamisen, sekä digitaalisen infrastruktuurin hankkeisiin. ' +
          'Perusta ideasi käyttäjän toimialaan ja kiinnostuksen kohteisiin.';
        break;
      case 'arvioija':
        systemInstruction = 
          'Olet Arvioija, tekoälyagentti, joka arvioi kriittisesti Digital Europe Program -rahoitusohjelmaan suunnattuja ideoita. ' +
          'Tehtäväsi on analysoida ideoiden vahvuudet, heikkoudet ja antaa rakentavia parannusehdotuksia. ' +
          'Arvioi ideoita erityisesti rahoitusohjelman kriteerien perusteella ja ota huomioon idean innovatiivisuus, toteutettavuus ja vaikuttavuus. ' +
          'Anna konkreettisia parannusehdotuksia, jotka auttavat käyttäjää jalostamaan ideastaan kilpailukykyisemmän.';
        break;
      case 'hakija':
        systemInstruction = 
          'Olet Hakija, tekoälyagentti, joka auttaa muotoilemaan ideoita virallisiksi hakemuksiksi Digital Europe Program -rahoitusohjelmaan. ' +
          'Tehtäväsi on luoda strukturoituja, vakuuttavia hakemuksia, jotka vastaavat ohjelman vaatimuksia. ' +
          'Kysy tarvittavia lisätietoja hakemuksen täydentämiseksi ja varmista, että hakemuksessa on kaikki tarvittavat osiot: ' +
          'projektin kuvaus, tavoitteet, työsuunnitelma, tulosmittarit, budjetti, kumppanit ja vaikutusten arviointi. ' +
          'Auta käyttäjää muotoilemaan vastaukset, jotka korostavat idean sopivuutta rahoitusohjelman tavoitteisiin.';
        break;
      case 'rahoittaja':
        systemInstruction = 
          'Olet Rahoittaja, tekoälyagentti, joka arvioi Digital Europe Program -rahoitushakemuksia rahoittajan näkökulmasta. ' +
          'Tehtäväsi on antaa yksityiskohtaista palautetta hakemuksista ja arvioida niiden kilpailukykyä rahoitusohjelmassa. ' +
          'Arvioi hakemuksia seuraavien kriteerien perusteella: relevanssi (merkitys ohjelman tavoitteille), vaikuttavuus, toteutettavuus, ' +
          'innovatiivisuus ja kustannustehokkuus. Anna numeerinen arvio (0-100) sekä yksityiskohtaista palautetta jokaisesta osiosta. ' +
          'Tarjoa konkreettisia parannusehdotuksia, jotka auttavat käyttäjää vahvistamaan hakemustaan.';
        break;
      default:
        systemInstruction = 
          'Olet tekoälyagentti, joka auttaa Digital Europe Program -rahoitusohjelmaan liittyvissä asioissa.';
    }

    // Kokoa lisätiedot kontekstiksi
    let context = '';
    if (data.domain) {
      context += `Käyttäjän toimiala: ${data.domain}\n`;
    }
    if (data.interests && data.interests.length > 0) {
      context += `Käyttäjän kiinnostuksen kohteet: ${data.interests.join(', ')}\n`;
    }
    if (data.projectDetails) {
      context += `Projektin tiedot: ${data.projectDetails}\n`;
    }
    if (data.ideaDetails) {
      context += `Idean tiedot: ${data.ideaDetails}\n`;
    }
    if (data.applicationDetails) {
      context += `Hakemuksen tiedot: ${data.applicationDetails}\n`;
    }

    // Tee API-kutsu
    const response = await openai.chat.completions.create({
      model: 'gpt-4-turbo-preview', // tai muu sopiva malli
      messages: [
        {
          role: 'system',
          content: systemInstruction
        },
        {
          role: 'user',
          content: context ? `${context}\n\n${prompt}` : prompt
        }
      ],
      max_tokens: 1000,
      temperature: role === 'ideanikkari' ? 0.8 : 0.5, // Ideanikkarille korkeampi luovuus
    });

    return response.choices[0].message.content;
  } catch (error) {
    console.error('OpenAI API -virhe:', error);
    throw new Error(`Tekoälykutsu epäonnistui: ${error.message}`);
  }
};

/**
 * Luo vastauksen Anthropic API:sta, jos OpenAI ei ole käytettävissä
 * @param {string} role - Agentin rooli
 * @param {string} prompt - Käyttäjän syöte
 * @param {object} data - Mahdolliset lisätiedot
 * @returns {Promise<string>} Tekoälyn vastaus
 */
exports.createAnthropicCompletion = async (role, prompt, data = {}) => {
  // Tähän voidaan toteuttaa Anthropic API -integraatio
  throw new Error('Anthropic API ei ole vielä tuettu');
};

/**
 * Palauttaa saatavilla olevat tekoälypalvelut
 * @returns {object} Saatavilla olevat palvelut
 */
exports.getAvailableServices = () => {
  const services = {
    openai: !!process.env.OPENAI_API_KEY,
    anthropic: !!process.env.ANTHROPIC_API_KEY,
    googleai: !!process.env.GOOGLE_AI_API_KEY
  };

  return services;
}; 